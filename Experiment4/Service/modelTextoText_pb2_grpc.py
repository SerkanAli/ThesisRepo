# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import modelTextoText_pb2 as modelTextoText__pb2


class RunElgServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.InitParameter = channel.unary_unary(
                '/RunElgService/InitParameter',
                request_serializer=modelTextoText__pb2.ELG_Parameter.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )
        self.RunElgService = channel.unary_unary(
                '/RunElgService/RunElgService',
                request_serializer=modelTextoText__pb2.ELG_Text.SerializeToString,
                response_deserializer=modelTextoText__pb2.ELG_Text.FromString,
                )


class RunElgServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def InitParameter(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RunElgService(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RunElgServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'InitParameter': grpc.unary_unary_rpc_method_handler(
                    servicer.InitParameter,
                    request_deserializer=modelTextoText__pb2.ELG_Parameter.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
            'RunElgService': grpc.unary_unary_rpc_method_handler(
                    servicer.RunElgService,
                    request_deserializer=modelTextoText__pb2.ELG_Text.FromString,
                    response_serializer=modelTextoText__pb2.ELG_Text.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RunElgService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RunElgService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def InitParameter(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RunElgService/InitParameter',
            modelTextoText__pb2.ELG_Parameter.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RunElgService(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RunElgService/RunElgService',
            modelTextoText__pb2.ELG_Text.SerializeToString,
            modelTextoText__pb2.ELG_Text.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
