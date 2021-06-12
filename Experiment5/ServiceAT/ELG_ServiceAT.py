from elg import Service
from elg import Authentication
import grpc
import json
from concurrent import futures
import time

import modelAudioToText_pb2
import modelAudioToText_pb2_grpc


port = 50084
ServiceIDs = []

class RunElgServiceServicer(modelAudioToText_pb2_grpc.RunElgServiceServicer):
    def InitParameter(self, request,context):
        global ServiceIDs
        response = modelAudioToText_pb2.ELG_TEXT()
        ServiceIDs = request.ServiceIDs
        print("Service ID is:", ServiceIDs)
        response.PlainText = "Everything OK"
        return response

    def RunElgService(self, request,context):
        response = modelAudioToText_pb2.ELG_Text()
        CurrentServiceID = request.Protocol.AfterServicesIDs[0]
        request.Protocol.AfterServicesIDs.pop(0)

        for ID in request.Protocol.AfterServicesIDs :
            response.Protocol.AfterServicesIDs.append(ID)

        auth = Authentication.from_json('authJSONFile')
        lt = Service.from_id(CurrentServiceID,auth)
        result = lt('AudioFiles/test.mp3')
        print(result['response']['texts'][0]['content'])
        response.PlainText = json.dumps(result['response']['texts'][0]['content'])
        return response



#test function
def SomeTesting():
    newService = RunElgServiceServicer()
    newReq = modelAudioToText_pb2.ELG_Audio()
    newReq.Protocol.BeforeServiceID = -1
    newReq.Protocol.CurrentServiceID = -1
    newReq.Protocol.AfterServicesIDs.append(489)
    newService.RunElgService(newReq, 'bla')


# creat a grpc server :
#SomeTesting()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

modelAudioToText_pb2_grpc.add_RunElgServiceServicer_to_server(RunElgServiceServicer(), server)
print("Starting Servcie Server. Listening to port :" + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)








