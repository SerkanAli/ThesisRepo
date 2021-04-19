import grpc

from . import databroker_pb2_grpc as bla

from google.protobuf import empty_pb2

def RunDatabroker():
    #speak first of all to the databroker
    port_DataBroker = 'localhost:50080'
    channel_DataBroker = grpc.insecure_channel(port_DataBroker)
    stub_Databroker = bla.Transfer_ELG_TextStub(channel_DataBroker)

    request_DataBroker = empty_pb2.Empty()
    response_DataBroker = stub_Databroker.get_Text(request_DataBroker)
    print(response_DataBroker)
    return response_DataBroker

RunDatabroker()