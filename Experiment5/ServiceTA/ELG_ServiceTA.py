from elg import Service
from elg import Authentication
from elg.model import *
import grpc
import json
from concurrent import futures
import time
from collections import Counter
from base64 import b64decode
from pathlib import Path

import modelTextoAudio_pb2
import modelTextoAudio_pb2_grpc


port = 50082
ServiceIDs = []

class RunElgServiceServicer():
    def InitParameter(self, request,context):
        global ServiceIDs
        response = modelTextoAudio_pb2.ELG_Text()
        ServiceIDs = request.ServiceIDs
        print("Service ID is:", ServiceIDs)
        response.PlainText = "Everything OK"
        return response

    def RunElgService(self, request,context):
        response = modelTextoAudio_pb2.ELG_Audio()
        CurrentServiceID = request.Protocol.AfterServicesIDs[0]
        request.Protocol.AfterServicesIDs.pop(0)

        for ID in request.Protocol.AfterServicesIDs :
            response.Protocol.AfterServicesIDs.append(ID)
        
        auth = Authentication.from_json('authJSONFile')
        lt = Service.from_id(CurrentServiceID,auth)  
        result = lt(TextRequest(content=request.PlainText))
        response.format = result.format
        response.content = result.content
        result.to_file('test_file.mp3')
        return response



#test function
def SomeTesting():
    newService = RunElgServiceServicer()
    newParam = modelTextoAudio_pb2.ELG_Parameter()
    newParam.ServiceIDs.append(4837)
    newService.InitParameter(newParam, 'bla')
    newReq = modelTextoAudio_pb2.ELG_Text()
    newReq.PlainText = 'Hello World. How are you today?'
    newReq.Protocol.BeforeServiceID = -1
    newReq.Protocol.CurrentServiceID = -1
    newReq.Protocol.AfterServicesIDs.append(4837)
    while True:
        response = newService.RunElgService(newReq, 'bla')
        newReq = response
        if Counter(response.Protocol.AfterServicesIDs) == Counter() :
            break
    filename = Path('filename_test.mp3')
    with open(filename, "wb") as f:
        f.write(b64decode(newReq.content))


# creat a grpc server :
#SomeTesting()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

modelTextoAudio_pb2_grpc.add_RunElgServiceServicer_to_server(RunElgServiceServicer(), server)
print("Starting Servcie Server. Listening to port :" + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)








