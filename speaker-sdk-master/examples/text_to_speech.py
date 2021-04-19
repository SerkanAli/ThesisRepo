# ***************************************************************************
#
#                  (C) Copyright Fraunhofer IIS 2020
#                          All Rights Reserved
#
#   This software and/or program is protected by copyright law and
#   international treaties. Any unauthorized reproduction or distribution
#   of this software and/or program, or any portion of it, may result in
#   severe civil and criminal penalties, and will be prosecuted to the
#   maximum extent possible under law.
#
# ***************************************************************************
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from getpass import getpass
from io import BytesIO
from pathlib import Path
from pprint import pprint
from queue import Empty, Queue
from threading import Event
from typing import Any, Text, Tuple

import click
import grpc
import numpy as np
import sounddevice as sd
import soundfile as sf
from google.protobuf.json_format import MessageToDict
from keycloak_login import KeyCloak
from speaker_sdk.speaker_pb2 import AudioFormat, TtsRequest
from speaker_sdk.speaker_pb2_grpc import TextToSpeechStub

DEFAULT_SPEECH = "Hello. I'm a virtual assistant.".split()
DEFAULT_HOST = "localhost:8000"
DEFAULT_LANGUAGE = "en-US"
DEFAULT_SAMPLERATE = 16000
DEFAULT_FORMAT = "pcm"
AUDIO_FORMATS = {
    "pcm": AudioFormat.Encoding.PCM16,
    "wav": AudioFormat.Encoding.WAV,
    "flac": AudioFormat.Encoding.FLAC,
}
CHUNK_SIZE = 4096


stop_event = Event()  # An event used to signal that the playback has stopped
audio_fifo: Queue  # A FIFO buffer for handling the audio chunks
playing = False  # A flag indicating whether the playback has started, yet


class AudioFifo(Queue):
    def __init__(self, chunk_size: int, channels: int = 1):
        assert channels == 1, "Currently only mono signals are supported"

        super().__init__()
        self.chunk_size = chunk_size
        self.channels = channels
        self.buffer = np.ndarray((0, channels), dtype=np.int16)

    def put(self, chunk: np.ndarray, block: bool = True, timeout=None) -> np.ndarray:
        """
        Puts a chunk of audio into the queue.

        If the chunk size is not dividable by the preferred chunk size the remainder is buffered
        and merged with the next chunk.

        To force any remaining partial chunk into the queue call .flush()
        """
        assert isinstance(
            chunk, np.ndarray
        ), f"chunk should be a numpy.ndarray but got {type(chunk)}"
        assert chunk.dtype == np.int16, "chunk dtype should be int16"
        assert chunk.ndim == 1 or chunk.shape[1] == 1, "Currently only mono signals are supported"

        if chunk.ndim == 1:
            # Reshape 1-dim signal to 2-dim
            chunk.shape = (-1, 1)

        self.buffer = np.vstack((self.buffer, chunk))

        while self.buffer.shape[0] >= self.chunk_size:
            super().put(self.buffer[: self.chunk_size])
            self.buffer = self.buffer[self.chunk_size :]

    def flush(self) -> None:
        """
        Flushes any remaining partial audio chunk into the queue.
        """
        super().put(self.buffer)
        self.buffer = np.ndarray((0, 1), dtype=np.int16)


def callback(outdata: np.ndarray, frames: int, time, status: sd.CallbackFlags) -> None:
    global audio_fifo, playing

    if status.output_underflow:
        print("Output underflow: increase blocksize?")
        raise sd.CallbackAbort

    assert not status

    try:
        data = audio_fifo.get_nowait()
    except Empty as e:
        if not playing:
            # Playback has not started yet, keep waiting.
            print("Playback buffer empty. Waiting for speech...")
            outdata[:] = 0
            return
        else:
            # Buffer is empty. This could mean that the loop took too long to fill the buffer but
            # since there is nothing here consuming computing time we assume that the playback
            # should be finished since there are no more chunks.
            print("Buffer is empty. Stopping playback.")
            raise sd.CallbackStop from e
    else:
        playing = True

    if len(data) < len(outdata):
        outdata[: len(data)] = data
        outdata[len(data) :] = np.zeros((len(outdata) - len(data), 1), dtype=np.int16)
    else:
        outdata[:] = data


@click.command()
@click.option(
    "--host", default=DEFAULT_HOST, show_default=True, help="Hostname of the text-to-speech server"
)
@click.option("--out", type=str, help="Save synthesized speech to file")
@click.option(
    "--format",
    default=DEFAULT_FORMAT,
    type=click.Choice(list(AUDIO_FORMATS.keys()), case_sensitive=False),
    show_default=True,
    help="Desired encoding of synthesized speech",
)
@click.option("--language", default=DEFAULT_LANGUAGE, show_default=True, help="Speech language")
@click.option(
    "--samplerate",
    default=DEFAULT_SAMPLERATE,
    type=int,
    show_default=True,
    help="Desired sampling rate of synthesized speech",
)
@click.option(
    "--jwt-file",
    default=None,
    type=click.Path(),
    help="Specify file containing a valid JWT token.",
)
@click.option(
    "-u", "--username", default=None, type=str, help="Username for authentication via KeyCloak"
)
@click.option(
    "-p",
    "--password",
    default=None,
    type=str,
    help="Password for authentication via KeyCloak. User will be prompted if --user flag was provided but --password was not.",
)
@click.option(
    "--insecure", is_flag=True, help="Accept insecure (unencrypted) incoming connections"
)
@click.option(
    "--auth_host",
    default="https://speaker-keycloak.185.128.119.217.xip.io",
    type=str,
    help="Host of the authentication server.",
)
@click.option(
    "--cert",
    type=click.Path(),
    default=Path("certs", "server.crt"),
    show_default=True,
    help="Location of certificate file",
)
@click.option(
    "--namespace",
    default=None,
    type=str,
    help="Namespace used for direct routing.")
@click.option(
    "--service",
    default=None,
    type=str,
    help="Name of the service used for direct routing."
)
@click.option(
    "--port",
    default="80",
    type=str,
    help="Port used for direct routing.")
@click.option("--debug", is_flag=True, help="Request debug information from service")
@click.argument("speech", nargs=-1, type=str)
def text_to_speech(
    host: Text,
    out: Text,
    format: Text,
    language: Text,
    samplerate: int,
    jwt_file: str,
    username: str,
    password: str,
    insecure: bool,
    auth_host: str,
    cert: str,
    namespace: str,
    service: str,
    port: str,
    debug: bool,
    speech: Tuple[Text],
) -> None:
    """
    Calls the text-to-speech service and requests to synthesize the speech given.

    If the chosen audio format is `pcm` then the speech is instantly played back as it is received.
    For any other value the returned audio file is buffered and played back after it has been fully
    received.

    The speech can be specified in the SPEECH argument.
    """
    global audio_fifo, CHUNK_SIZE

    CHUNK_SIZE = samplerate // 10
    audio_fifo = AudioFifo(CHUNK_SIZE)

    if not speech:
        speech = DEFAULT_SPEECH

    print(f"       Speech: {speech}")
    print(f"         Host: {host}")
    print(f"Sampling rate: {samplerate}")
    if out:
        print("Saving speech to '{args.out}'")
    print()

    count = 1  # packet counter
    audio = b""  # buffer where the audio data is collected

    if insecure:
        channel = grpc.insecure_channel(host)
    else:
        with open(cert, "rb") as f:
            creds = grpc.ssl_channel_credentials(f.read())
        channel = grpc.secure_channel(host, creds)

    access_token = ""

    if jwt_file:
        try:
            access_token = open(jwt_file).read()
        except Exception as e:
            print("Error reading jwt file: %s" % e)
    else:
        if username and not password:
            password = getpass()
        keycloak = KeyCloak(auth_host=auth_host, cert=cert)
        access_token = keycloak.login(username, password)["access_token"]

    print("Using access_token: %s" % access_token)

    with channel as ctx:
        tts = TextToSpeechStub(ctx)

        if format == "pcm":
            # With PCM we can instantly play back the synthesized speech
            stream = sd.OutputStream(
                samplerate=samplerate,
                blocksize=CHUNK_SIZE,
                channels=1,
                dtype=np.int16,
                callback=callback,
                finished_callback=stop_event.set,
            )
            with stream:
                print("Synthesizing and instantly playing back speech...")
                for response in tts.synthesize(
                    TtsRequest(
                        text=" ".join(speech),
                        language=language,
                        audio_format=AudioFormat(
                            encoding=AUDIO_FORMATS[format], samplerate=samplerate
                        ),
                        debug=debug,
                    ),
                    metadata=[
                        ("accesstoken", access_token),
                        ("namespace", namespace),
                        ("service", service),
                        ("port", port),
                    ],
                ):
                    print(f"Received audio chunk #{count} ({len(response.audio)} bytes)")
                    audio_fifo.put(np.frombuffer(response.audio, dtype=np.int16))
                    if out:
                        # Buffer the speech only if it should be saved into a file
                        audio += response.audio
                    count += 1

                    if response.HasField("debug_info"):
                        print("#### DEBUG INFO ####")
                        pprint(MessageToDict(response.debug_info))
                        print("#" * 20)

                audio_fifo.flush()
                stop_event.wait()
        else:
            # Some other format than PCM is buffered and played back after the whole file is
            # received.
            print("Synthesizing speech...")
            for response in tts.synthesize(
                TtsRequest(
                    text=" ".join(speech),
                    language=language,
                    audio_format=AudioFormat(
                        encoding=AUDIO_FORMATS[format], samplerate=samplerate
                    ),
                    debug=debug,
                ),
                metadata=[
                    ("accesstoken", access_token),
                    ("namespace", namespace),
                    ("service", service),
                    ("port", port),
                ],
            ):
                print(f"Received audio chunk #{count} ({len(response.audio)} bytes)")
                audio += response.audio
                count += 1

                if response.HasField("debug_info"):
                    print("#### DEBUG INFO ####")
                    pprint(MessageToDict(response.debug_info))
                    print("#" * 20)

            print("Playing back speech...")
            playback_audio, samplerate = sf.read(BytesIO(audio), dtype="int16")
            sd.play(playback_audio, samplerate=samplerate, blocking=True)

    if out and audio:
        # Save the synthesized speech to a file
        print(f"Saving {len(audio)} bytes to {out}")
        with open(out, "wb") as f:
            f.write(audio)

    print("Done.")


if __name__ == "__main__":
    text_to_speech()
