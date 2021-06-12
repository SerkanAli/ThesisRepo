import grpc
import modelTextoText_pb2
import modelTextoText_pb2_grpc
from google.protobuf import empty_pb2


def RunServiceWithParameter(PlainText, ServiceID):
    port_Service = 'localhost:50082'
    channel_Service = grpc.insecure_channel(port_Service)
    stub_Service = modelTextoText_pb2_grpc.RunElgServiceStub(channel_Service)

    request = modelTextoText_pb2.ELG_Parameter()
    request.ServiceID = ServiceID
    stub_Service.InitParameter(request)

    request_Text = modelTextoText_pb2.ELG_Text()
    request_Text.PlainText = PlainText
    response_Service = stub_Service.RunElgService(request_Text)
    print('Response from Service:', response_Service)
    return response_Service
    


RunServiceWithParameter('How about today?', 515)