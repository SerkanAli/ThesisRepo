import grpc

import databroker_pb2_grpc

from google.protobuf import empty_pb2

def RunDatabroker():
    #speak first of all to the databroker
    port_DataBroker = 'localhost:8061'
    channel_DataBroker = grpc.insecure_channel(port_DataBroker)
    stub_Databroker = databroker_pb2_grpc.Transfer_ELG_TextStub(channel_DataBroker)

    request_DataBroker = empty_pb2.Empty()
    response_DataBroker = stub_Databroker.get_Text(request_DataBroker)
    print(response_DataBroker)
    return response_DataBroker

RunDatabroker()