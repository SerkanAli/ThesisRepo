import grpc
from concurrent import futures
import time

import parameter_pb2
import parameter_pb2_grpc

port = 50081

class Transfer_ELG_ParameterServicer(parameter_pb2_grpc.Transfer_ELG_ParameterServicer):
    def get_ServcieID(self, request, context):
        response = parameter_pb2.ELG_Parameter()
        response.ServiceID = 515
        print('Service sending is ID 515')
        return response



# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

parameter_pb2_grpc.add_Transfer_ELG_ParameterServicer_to_server(Transfer_ELG_ParameterServicer(), server)
print("Starting Parameter Server. Listening to port :" + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
