import grpc
from concurrent import futures
import time

import databroker_pb2
import databroker_pb2_grpc

port = 8061


class Transfer_ELG_TextServicer(databroker_pb2_grpc.Transfer_ELG_TextServicer):
    def get_Text(self, request, context):
        response = databroker_pb2.ELG_Text()
        response.PlainText = 'Hello World. How are you today and what are you doing tomorrow?'
        print(response)
        return response


# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

databroker_pb2_grpc.add_Transfer_ELG_TextServicer_to_server(Transfer_ELG_TextServicer(), server)
print("Starting Databroker Server. Listening to port :" + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
