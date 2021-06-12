from elg import Service
from elg import Authentication
import grpc
import json
from concurrent import futures
import time

import modelTextoText_pb2
import modelTextoText_pb2_grpc


port = 8061
ServiceID = 515

class RunElgServiceServicer():
    def InitParameter(self, request,context):
        global ServiceID
        response = modelTextoText_pb2.ELG_Text()
        ServiceID = request.ServiceID
        print("Service ID is:", ServiceID)
        response.PlainText = "Everything OK"
        return response

    def RunElgService(self, request,context):
        global ServiceID
        response = modelTextoText_pb2.ELG_Text()
        auth = Authentication.from_json('authJSONFile')
        ServiceID = 515
        lt = Service.from_id(ServiceID,auth)
        result = lt(request.PlainText)
        print(result['response']['annotations'])
        response.PlainText = json.dumps(result)
        return response



#test function
def SomeTesting():
    newService = RunElgServiceServicer()
    newParam = modelTextoText_pb2.ELG_Parameter()
   # newParam.ServiceID = 515
    newService.InitParameter(newParam, 'bla')
    newReq = modelTextoText_pb2.ELG_Text()
    newReq.PlainText = 'Hello World today'
    newService.RunElgService(newReq, 'bla')


# creat a grpc server :
SomeTesting()
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








