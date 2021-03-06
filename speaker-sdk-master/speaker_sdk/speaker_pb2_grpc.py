# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from speaker_sdk import speaker_pb2 as speaker__sdk_dot_speaker__pb2


class SpeechRecognitionStub(object):
    """*
    This service provides an interface for recognizing and transcribing speech
    which has been recorded from the user.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.transcribe = channel.stream_stream(
                '/speaker.beta2.SpeechRecognition/transcribe',
                request_serializer=speaker__sdk_dot_speaker__pb2.SpeechRecognitionRequest.SerializeToString,
                response_deserializer=speaker__sdk_dot_speaker__pb2.Transcript.FromString,
                )


class SpeechRecognitionServicer(object):
    """*
    This service provides an interface for recognizing and transcribing speech
    which has been recorded from the user.
    """

    def transcribe(self, request_iterator, context):
        """Transcribe the passed audio stream
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SpeechRecognitionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'transcribe': grpc.stream_stream_rpc_method_handler(
                    servicer.transcribe,
                    request_deserializer=speaker__sdk_dot_speaker__pb2.SpeechRecognitionRequest.FromString,
                    response_serializer=speaker__sdk_dot_speaker__pb2.Transcript.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'speaker.beta2.SpeechRecognition', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SpeechRecognition(object):
    """*
    This service provides an interface for recognizing and transcribing speech
    which has been recorded from the user.
    """

    @staticmethod
    def transcribe(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/speaker.beta2.SpeechRecognition/transcribe',
            speaker__sdk_dot_speaker__pb2.SpeechRecognitionRequest.SerializeToString,
            speaker__sdk_dot_speaker__pb2.Transcript.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class DialogueManagerStub(object):
    """*
    This service handles incoming textual queries from the user or possibly
    other events which may be triggered by some devices.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.handle = channel.unary_unary(
                '/speaker.beta2.DialogueManager/handle',
                request_serializer=speaker__sdk_dot_speaker__pb2.DialogueRequest.SerializeToString,
                response_deserializer=speaker__sdk_dot_speaker__pb2.DialogueResponse.FromString,
                )


class DialogueManagerServicer(object):
    """*
    This service handles incoming textual queries from the user or possibly
    other events which may be triggered by some devices.
    """

    def handle(self, request, context):
        """Predict a response to the user input.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_DialogueManagerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'handle': grpc.unary_unary_rpc_method_handler(
                    servicer.handle,
                    request_deserializer=speaker__sdk_dot_speaker__pb2.DialogueRequest.FromString,
                    response_serializer=speaker__sdk_dot_speaker__pb2.DialogueResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'speaker.beta2.DialogueManager', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class DialogueManager(object):
    """*
    This service handles incoming textual queries from the user or possibly
    other events which may be triggered by some devices.
    """

    @staticmethod
    def handle(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/speaker.beta2.DialogueManager/handle',
            speaker__sdk_dot_speaker__pb2.DialogueRequest.SerializeToString,
            speaker__sdk_dot_speaker__pb2.DialogueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class TextToSpeechStub(object):
    """*
    This service synthesizes speech from a given text.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.synthesize = channel.unary_stream(
                '/speaker.beta2.TextToSpeech/synthesize',
                request_serializer=speaker__sdk_dot_speaker__pb2.TextToSpeechRequest.SerializeToString,
                response_deserializer=speaker__sdk_dot_speaker__pb2.SynthesizedSpeech.FromString,
                )


class TextToSpeechServicer(object):
    """*
    This service synthesizes speech from a given text.
    """

    def synthesize(self, request, context):
        """Synthesize the given text as natural language
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TextToSpeechServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'synthesize': grpc.unary_stream_rpc_method_handler(
                    servicer.synthesize,
                    request_deserializer=speaker__sdk_dot_speaker__pb2.TextToSpeechRequest.FromString,
                    response_serializer=speaker__sdk_dot_speaker__pb2.SynthesizedSpeech.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'speaker.beta2.TextToSpeech', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TextToSpeech(object):
    """*
    This service synthesizes speech from a given text.
    """

    @staticmethod
    def synthesize(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/speaker.beta2.TextToSpeech/synthesize',
            speaker__sdk_dot_speaker__pb2.TextToSpeechRequest.SerializeToString,
            speaker__sdk_dot_speaker__pb2.SynthesizedSpeech.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class VoiceAssistantStub(object):
    """This is the voice assistant service which provides a single interface to conveniently access all
    the other services during a conversation with the user. It bundles all three regular calls of a
    voice interaction, to the speech recognizer, the dialogue manager and the speech synthesizer,
    into one call.

    Each call represents a single turn in the conversation between the user and the voice assistant
    and consists of one or more streamed requests and responses between client and server.

    #### Examples

    This is an example for one turn using the full voice assistant, i.e. sending audio in and
    receiving audio back:
    * [IN] AssistantRequest.config
    * [IN] AssistantRequest.audio_in
    * [IN] AssistantRequest.audio_in
    * [OUT] AssistantResponse.transcript
    * [IN] AssistantRequest.audio_in
    * [IN] AssistantRequest.audio_in
    * [OUT] AssistantResponse.transcript
    * [OUT] AssistantResponse.response
    * [OUT] AssistantResponse.events
    * [OUT] AssistantResponse.speech
    * [OUT] AssistantResponse.speech
    * [OUT] AssistantResponse.speech

    Also a chatbot behaviour can be configured if the `AssistantConfig.text_query` field is set and
    no `audio_out` configuration is provided:

    * [IN] AssistantRequest.config
    * [OUT] AssistantResponse.response
    * [OUT] AssistantResponse.events
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.assist = channel.stream_stream(
                '/speaker.beta2.VoiceAssistant/assist',
                request_serializer=speaker__sdk_dot_speaker__pb2.AssistantRequest.SerializeToString,
                response_deserializer=speaker__sdk_dot_speaker__pb2.AssistantResponse.FromString,
                )


class VoiceAssistantServicer(object):
    """This is the voice assistant service which provides a single interface to conveniently access all
    the other services during a conversation with the user. It bundles all three regular calls of a
    voice interaction, to the speech recognizer, the dialogue manager and the speech synthesizer,
    into one call.

    Each call represents a single turn in the conversation between the user and the voice assistant
    and consists of one or more streamed requests and responses between client and server.

    #### Examples

    This is an example for one turn using the full voice assistant, i.e. sending audio in and
    receiving audio back:
    * [IN] AssistantRequest.config
    * [IN] AssistantRequest.audio_in
    * [IN] AssistantRequest.audio_in
    * [OUT] AssistantResponse.transcript
    * [IN] AssistantRequest.audio_in
    * [IN] AssistantRequest.audio_in
    * [OUT] AssistantResponse.transcript
    * [OUT] AssistantResponse.response
    * [OUT] AssistantResponse.events
    * [OUT] AssistantResponse.speech
    * [OUT] AssistantResponse.speech
    * [OUT] AssistantResponse.speech

    Also a chatbot behaviour can be configured if the `AssistantConfig.text_query` field is set and
    no `audio_out` configuration is provided:

    * [IN] AssistantRequest.config
    * [OUT] AssistantResponse.response
    * [OUT] AssistantResponse.events
    """

    def assist(self, request_iterator, context):
        """This is a convenience function for interacting with the speech assistant.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_VoiceAssistantServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'assist': grpc.stream_stream_rpc_method_handler(
                    servicer.assist,
                    request_deserializer=speaker__sdk_dot_speaker__pb2.AssistantRequest.FromString,
                    response_serializer=speaker__sdk_dot_speaker__pb2.AssistantResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'speaker.beta2.VoiceAssistant', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class VoiceAssistant(object):
    """This is the voice assistant service which provides a single interface to conveniently access all
    the other services during a conversation with the user. It bundles all three regular calls of a
    voice interaction, to the speech recognizer, the dialogue manager and the speech synthesizer,
    into one call.

    Each call represents a single turn in the conversation between the user and the voice assistant
    and consists of one or more streamed requests and responses between client and server.

    #### Examples

    This is an example for one turn using the full voice assistant, i.e. sending audio in and
    receiving audio back:
    * [IN] AssistantRequest.config
    * [IN] AssistantRequest.audio_in
    * [IN] AssistantRequest.audio_in
    * [OUT] AssistantResponse.transcript
    * [IN] AssistantRequest.audio_in
    * [IN] AssistantRequest.audio_in
    * [OUT] AssistantResponse.transcript
    * [OUT] AssistantResponse.response
    * [OUT] AssistantResponse.events
    * [OUT] AssistantResponse.speech
    * [OUT] AssistantResponse.speech
    * [OUT] AssistantResponse.speech

    Also a chatbot behaviour can be configured if the `AssistantConfig.text_query` field is set and
    no `audio_out` configuration is provided:

    * [IN] AssistantRequest.config
    * [OUT] AssistantResponse.response
    * [OUT] AssistantResponse.events
    """

    @staticmethod
    def assist(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/speaker.beta2.VoiceAssistant/assist',
            speaker__sdk_dot_speaker__pb2.AssistantRequest.SerializeToString,
            speaker__sdk_dot_speaker__pb2.AssistantResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
