import grpc
import modelTextoAudio_pb2
import modelTextoAudio_pb2_grpc
from collections import Counter
from base64 import b64decode
from pathlib import Path


def RunServiceWithParameter(PlainText, ServiceID):
    port_Service = 'localhost:50082'
    channel_Service = grpc.insecure_channel(port_Service)
    stub_Service = modelTextoAudio_pb2_grpc.RunElgServiceStub(channel_Service)

    newParam = modelTextoAudio_pb2.ELG_Parameter()
    newParam.ServiceIDs.append(4837)
    stub_Service.InitParameter(newParam)
    newReq = modelTextoAudio_pb2.ELG_Text()
    newReq.PlainText = 'Hello World. How are you today?'
    newReq.Protocol.BeforeServiceID = -1
    newReq.Protocol.CurrentServiceID = -1
    newReq.Protocol.AfterServicesIDs.append(4837)
    while True:
        response = stub_Service.RunElgService(newReq)
        newReq = response
        if Counter(response.Protocol.AfterServicesIDs) == Counter() :
            break
    filename = Path('filename_test.mp3')
    with open(filename, "wb") as f:
        f.write(b64decode(newReq.content))
    


RunServiceWithParameter('How about today?', 515)