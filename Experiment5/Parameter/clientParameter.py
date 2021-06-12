import grpc
import parameter_pb2_grpc
from google.protobuf import empty_pb2

def RunParameter():
    port_Parameter = 'localhost:50081'
    channel_Parameter = grpc.insecure_channel(port_Parameter)
    stub_Parameter = parameter_pb2_grpc.Transfer_ELG_ParameterStub(channel_Parameter)

    request_Parameter = empty_pb2.Empty()
    response_Parameter = stub_Parameter.get_ServcieID(request_Parameter)
    print(response_Parameter)
    return response_Parameter


RunParameter()