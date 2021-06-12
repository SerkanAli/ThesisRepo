import grpc
import modelAudioToText_pb2
import modelAudioToText_pb2_grpc
from google.protobuf import empty_pb2


def RunServiceWithParameter(PlainText, ServiceID):
    port_Service = 'localhost:50084'
    channel_Service = grpc.insecure_channel(port_Service)
    stub_Service = modelAudioToText_pb2_grpc.RunElgServiceStub(channel_Service)

    newReq = modelAudioToText_pb2.ELG_Audio()
    newReq.Protocol.BeforeServiceID = -1
    newReq.Protocol.CurrentServiceID = -1
    newReq.Protocol.AfterServicesIDs.append(489)

    response_Service = stub_Service.RunElgService(newReq)
    print('Response from Service:', response_Service.PlainText)
    return response_Service
    


RunServiceWithParameter('How about today?', 489)