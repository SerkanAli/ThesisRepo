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

import asyncio
import logging
import os
import platform
import signal
from io import BytesIO
from uuid import uuid4

import click
import grpc
import soundfile as sf
from google.protobuf.json_format import ParseDict
from google.protobuf.struct_pb2 import Struct
from grpc import aio
import samplerate

from speaker_sdk.speaker_pb2 import (
    AudioFormat,
    DialogueRequest,
    DialogueResponse,
    SynthesizedSpeech,
    Transcript,
)
from speaker_sdk.speaker_pb2_grpc import (
    DialogueManagerServicer,
    SpeechRecognitionServicer,
    TextToSpeechServicer,
    add_DialogueManagerServicer_to_server,
    add_SpeechRecognitionServicer_to_server,
    add_TextToSpeechServicer_to_server,
)

DEFAULT_PORT = 50000  # default host port to listen for incoming requests
stop_event = asyncio.Event()  # an event signalling to shut down
logger = logging.getLogger("mockup")


class AsrMockup(SpeechRecognitionServicer):
    logger = logging.getLogger("asr-mockup")

    SUPPORTED_LANGUAGES = ("en-US", "en-GB", "de-DE")
    UTTERANCES = {
        "en-US": "Hello. How are you today?".split(),
        "en-GB": "Hello. How are you today?".split(),
        "de-DE": "Hallo. Wie geht es dir heute?".split(),
    }

    CONTENT_TYPE_MAP = {
        AudioFormat.Encoding.WAV: "audio/x-wav",
        AudioFormat.Encoding.FLAC: "audio/x-flac",
    }

    async def transcribe(self, request_iterator, context):
        it = request_iterator.__aiter__()

        try:
            request = await it.__anext__()
        except StopAsyncIteration:
            self.logger.debug("Call cancelled prematurely")
            return

        if request.HasField("config"):
            config = request.config
        else:
            raise aio.AioRpcError(
                grpc.StatusCode.INVALID_ARGUMENT,
                "First message has to contain the config field",
            )

        if config.language not in self.SUPPORTED_LANGUAGES:
            await context.abort(
                grpc.StatusCode.INVALID_ARGUMENT,
                f"Language not supported: {config.language}; supported languages are: {self.SUPPORTED_LANGUAGES}",
            )

        k = 0
        async for request in it:
            k += 1

            transcript = " ".join(self.UTTERANCES[config.language][:k])

            if config.intermediate_results:
                yield Transcript(text=transcript, utterance_finished=False)

            # If we have reached the end of the utterance return a final transcript
            if k == len(self.UTTERANCES[config.language]):
                k = 0
                yield Transcript(text=transcript, utterance_finished=True)

                if not config.multiple_utterances:
                    break


class EchoDialogueManager(DialogueManagerServicer):
    """
    Simple dialogue manager implementation which just echoes back the user's input.
    """

    logger = logging.getLogger("dm-mockup")

    async def handle(
        self, request: DialogueRequest, context: grpc.ServicerContext
    ) -> DialogueResponse:
        text = request.text  # user's query (str)
        tracker = uuid4().bytes  # dialog state (byte array)

        return DialogueResponse(
            events=[
                DialogueResponse.EventOut(text=text),
                DialogueResponse.EventOut(
                    event=ParseDict(
                        {
                            "event": "play",
                            "device": "mediaplayer",
                            "song_name": "someone like you",
                        },
                        Struct(),
                    )
                ),
            ],
            tracker=tracker,
        )


class TtsMockup(TextToSpeechServicer):
    """
    This service is just a mockup for the Text-to-Speech service which provides the same speech for
    each and every call to it.
    """

    AUDIO_FORMATS = {
        AudioFormat.Encoding.WAV: {"format": "wav", "subtype": "PCM_16"},
        AudioFormat.Encoding.FLAC: {"format": "flac", "subtype": "PCM_16"},
    }

    CACHE_PATH = os.path.join(os.path.dirname(__file__), "cache")
    CHUNK_SIZE = 4096
    logger = logging.getLogger("tts-mockup")

    async def synthesize(self, request, context):
        """
        (See interface specification.)
        """
        audio_src, samplerate_orig = sf.read(os.path.join(self.CACHE_PATH, "hello.wav"))

        audio = samplerate.resample(
            audio_src,
            request.audio_format.samplerate / float(samplerate_orig),
            "sinc_best",
        )
        bio = BytesIO()
        sf.write(
            bio,
            audio,
            request.audio_format.samplerate,
            format=self.AUDIO_FORMATS[request.audio_format.encoding]["format"],
            subtype=self.AUDIO_FORMATS[request.audio_format.encoding]["subtype"],
        )
        bio.seek(0)
        audio_out = bio.read()

        for k in range(0, len(audio_out), self.CHUNK_SIZE):
            yield SynthesizedSpeech(audio=audio_out[k : k + self.CHUNK_SIZE])


def exit_gracefully(signum, frame) -> None:
    """
    Helper function which gets called when SIGINT or SIGTERM signal is received.
    It sets an event which causes the server to shutdown.
    """
    logger.info("Gracefully shutting down")
    asyncio.get_event_loop().call_soon_threadsafe(stop_event.set)


@click.command()
@click.option(
    "--port",
    default=DEFAULT_PORT,
    show_default=True,
    help="Port to listen for incoming requests",
)
def start(port: int) -> None:
    """
    This is a composite service which provides mockups for the three services SpeechRecognition,
    DialogueManager and TextToSpeech.
    """
    aio.init_grpc_aio()

    # Catch interrupt and termination signals
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    server = aio.server()
    add_SpeechRecognitionServicer_to_server(AsrMockup(), server)
    add_DialogueManagerServicer_to_server(EchoDialogueManager(), server)
    add_TextToSpeechServicer_to_server(TtsMockup(), server)

    logger.info("Service running on [::]:%d", port)
    server.add_insecure_port(f"[::]:{port}")
    asyncio.get_event_loop().run_until_complete(run(server, stop_event))

    logger.info("Bye")


async def periodic_wakeup():
    """
    This is a workaround because the select() call is not interruptable in the Python Windows
    implementation. By periodically waking up the event queue the KeyboardInterrupt exception can
    get triggered when the user pressed CTRL+C.
    """
    while True:
        await asyncio.sleep(1)


async def run(server, stop_event: asyncio.Event) -> None:
    if platform.system() == "Windows":
        asyncio.ensure_future(periodic_wakeup())

    await server.start()
    await asyncio.wait(
        {server.wait_for_termination(), stop_event.wait()},
        return_when=asyncio.FIRST_COMPLETED,
    )
    await server.stop(grace=0)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger("numba").setLevel(logging.WARN)

    start()
