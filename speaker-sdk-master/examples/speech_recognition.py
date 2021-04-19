#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

from getpass import getpass
from pathlib import Path
from pprint import pprint
from queue import Queue
from time import sleep
from typing import Text

import click
import grpc
import numpy as np
import sounddevice as sd
import soundfile as sf
from google.protobuf.json_format import MessageToDict
from keycloak_login import KeyCloak
from speaker_sdk.speaker_pb2 import AudioFormat, SpeechRecognitionRequest
from speaker_sdk.speaker_pb2_grpc import SpeechRecognitionStub

DEFAULT_LANGUAGE = "en-US"
DEFAULT_HOST = "localhost:50000"
DEFAULT_SAMPLERATE = 16000
DEFAULT_CHUNKS_PER_SECOND = 5

CONTENT_TYPE_MAP = {".wav": AudioFormat.Encoding.WAV, ".flac": AudioFormat.Encoding.FLAC}


@click.command()
@click.option(
    "--host",
    default=DEFAULT_HOST,
    show_default=True,
    help="Hostname of the speech recognition service",
)
@click.option(
    "--language",
    default=DEFAULT_LANGUAGE,
    show_default=True,
    help="BCP-47 code of language to be used",
)
@click.option(
    "--samplerate",
    default=DEFAULT_SAMPLERATE,
    type=int,
    show_default=True,
    help="Samplerate used for audio recording",
)
@click.option(
    "--chunks-per-second",
    default=DEFAULT_CHUNKS_PER_SECOND,
    show_default=True,
    help="The number of audio chunks sent per second",
)
@click.option(
    "-n",
    "--dummy",
    is_flag=True,
    default=False,
    help="Do not record anything. Instead, send fake audio chunks to the server",
)
@click.option(
    "--multiple-utterances",
    is_flag=True,
    default=False,
    help="Do not stop after the first utterance is finished but transcribe as long as audio input "
    "is sent",
)
@click.option(
    "--file",
    default=None,
    type=str,
    help="Specify an audio file that is sent to the server to be transcribed.",
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
def live_transcription(
    host: Text,
    language: Text,
    samplerate: int,
    chunks_per_second: int,
    dummy: bool,
    multiple_utterances: bool,
    file: Text,
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
) -> None:
    """
    Records audio from the system default audio input device and streams it to the speach
    recognizer. The final transcript is printed out as well as any intermediate transcripts during
    the recording.

    There is also the possibility of a dry run, where no audio is recorded. These options are
    only useful to test the speech recognizer mockup or eventually debug connectivity problems.
    One option is sending dummy values to the speech recognizer.
    Another possibility is sending an input file. This works only with small file sizes due to the
    grpc message size limit. Example files are in the folder './cache'.
    """

    q: Queue = Queue()
    send_audio = True
    chunk_size = samplerate // chunks_per_second

    config = SpeechRecognitionRequest(
        config=SpeechRecognitionRequest.Config(
            language=language,
            intermediate_results=True,
            multiple_utterances=multiple_utterances,
            audio_format=AudioFormat(encoding=AudioFormat.Encoding.PCM16, samplerate=samplerate),
            debug=debug,
        )
    )

    def audio_gen():
        """
        Generator function which sends the configuration and the stream of recorded audio blocks to
        the speech recognizer.

        The audio blocks are received from a queue which is fed by the audio callback function down
        below.
        """
        # The first message of the request stream has to be the configuration
        yield config

        while send_audio:
            audio = q.get()
            if audio is None:
                break

            yield SpeechRecognitionRequest(audio=audio.tobytes())

    def dummy_gen():
        """
        Generator for dummy audio chunks. This generator works the same way as the one above except
        that the generated audio chunks only contain dummy values.
        """
        # first send config
        yield config

        # then send audio
        k = 0
        while send_audio:
            yield SpeechRecognitionRequest(audio=b"X" * chunk_size)
            k += 1
            sleep(1.0 / chunks_per_second)

    def file_gen():
        """
        Generator for input file. This generator sends one small input file without splitting up
        the audio.
        """
        data, file_samplerate = sf.read(Path(file), dtype="int16")

        # if the audio file has more than one channel, only use the first channel
        if data.ndim > 1:
            data = data[:, 0]

        # first send config
        config.config.audio_format.samplerate = file_samplerate
        yield config

        # then send audio
        for k in range(0, len(data), chunk_size):
            yield SpeechRecognitionRequest(audio=data[k : k + chunk_size].tobytes())

        # keep sending silence to trigger endpointing
        while True:
            yield SpeechRecognitionRequest(audio=data[k : k + chunk_size].tobytes())
            sleep(1.0 / chunks_per_second)

    def audio_callback(indata, frames, time, status):
        """
        Callback function which is invoked every time a complete audio block is available from the
        microphone.
        """
        if status:
            print(f"Error in audio stream callback: {status}")

        q.put(indata.copy())

    if insecure:
        grpc_channel = grpc.insecure_channel(host)
    else:
        with open(cert, "rb") as f:
            creds = grpc.ssl_channel_credentials(f.read())
        grpc_channel = grpc.secure_channel(host, creds)

    access_token = ""

    if jwt_file:
        try:
            access_token = open(jwt_file).read()
        except Exception as e:
            print("Error reading jwt file: %s" % e)
    else:
        if username:
            if not password:
                password = getpass()
            keycloak = KeyCloak(auth_host=auth_host, cert=cert)
            access_token = keycloak.login(username, password)["access_token"]

    print("Using access_token: %s" % access_token)

    with grpc_channel as channel:
        asr = SpeechRecognitionStub(channel)

        if dummy or file:
            if dummy:
                print("*** Dry run ***")
                it = dummy_gen()
            else:
                print("*** Send file ***")
                it = file_gen()

            for transcript in asr.transcribe(
                it,
                metadata=[
                    ("accesstoken", access_token),
                    ("namespace", namespace),
                    ("service", service),
                    ("port", port),
                ],
            ):
                if transcript.utterance_finished:
                    print(f"Transcript: '{transcript.text}'")
                    print("---- Utterance Finished ----\n")

                    if not multiple_utterances:
                        send_audio = False
                else:
                    print(f"Intermediate transcript: '{transcript.text}'")

                if transcript.HasField("debug_info"):
                    print("#### DEBUG INFO ####")
                    pprint(MessageToDict(transcript.debug_info))
                    print("#" * 20)

        else:
            # Open an input stream from the default input audio device and print and receive the
            # transcripts from the speech recognizer.
            with sd.InputStream(
                samplerate=samplerate,
                blocksize=chunk_size,
                channels=1,
                callback=audio_callback,
                dtype=np.int16,
            ):
                print("#" * 80)
                print("Running in live transcription mode.")
                print("Press Ctrl+C to stop the recording")
                print("#" * 80)

                for transcript in asr.transcribe(
                    audio_gen(),
                    metadata=[
                        ("accesstoken", access_token),
                        ("namespace", namespace),
                        ("service", service),
                        ("port", port),
                    ],
                ):
                    if transcript.utterance_finished:
                        print(f"Transcript: '{transcript.text}'")
                        print("---- Utterance Finished ----\n")

                        if not multiple_utterances:
                            send_audio = False
                    else:
                        print(f"Intermediate transcript: '{transcript.text}'")

                    if transcript.HasField("debug_info"):
                        print("#### DEBUG INFO ####")
                        pprint(MessageToDict(transcript.debug_info))
                        print("#" * 20)


if __name__ == "__main__":
    try:
        live_transcription()
    except KeyboardInterrupt:
        print("\nBye")
