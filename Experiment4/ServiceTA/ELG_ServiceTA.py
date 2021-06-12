from elg import Service
from elg import Authentication
import grpc
import json
from concurrent import futures
import time

import modelTextoAudio_pb2
import modelTextoAudio_pb2_grpc


port = 50082
ServiceID = -1

class RunElgServiceServicer(modelTextoText_pb2_grpc.RunElgServiceServicer):
    def InitParameter(self, request,context):
        global ServiceID
        response = modelTextoAudio_pb2.Empty()
        ServiceID = request.ServiceID
        print("Service ID is:", ServiceID)
        return response

    def RunElgService(self, request,context):
        response = modelTextoAudio_pb2.ELG_Audio()
        auth = Authentication.from_json('authJSONFile')
        lt = Service.from_id(ServiceID,auth)
        result = lt(request.PlainText)
        print(result['response']['annotations'])
        response.content = json.dumps(result)
        return response



#test function
def SomeTesting():
    newService = RunElgServiceServicer()
    newParam = modelTextoAudio_pb2.ELG_Parameter()
    newParam.ServiceID = 515
    newService.InitParameter(newParam, 'bla')
    newReq = modelTextoAudio_pb2.ELG_Text()
    newReq.PlainText = 'Hello World. How are you today?'
    newService.RunElgService(newReq, 'bla')


# creat a grpc server :
#SomeTesting()
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

modelTextoText_pb2_grpc.add_RunElgServiceServicer_to_server(RunElgServiceServicer(), server)
print("Starting Servcie Server. Listening to port :" + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)








