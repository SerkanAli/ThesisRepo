import grpc
from concurrent import futures
import time

import databroker_pb2
import databroker_pb2_grpc

port = 8061


class Transfer_ELG_TextServicer():
    def get_Text(self, request, context):
        newReq = databroker_pb2.ELG_Text()
        newReq.PlainText = 'Meistens ist der Stoff eine grünlich glasige Masse aus geschmolzenem Quarz und Feldspat. Hallo, nebensatz!. Teile der Schmelzmassen allerdings enthalten große Mengen Metalle, die aus der verdampften Infrastruktur stammen'
        newReq.Protocol.BeforeServiceID = -1
        newReq.Protocol.CurrentServiceID = -1
       # newReq.Protocol.AfterServicesIDs.append(4840)
       # newReq.Protocol.AfterServicesIDs.append(4885)
        newReq.Protocol.AfterServicesIDs.append(478)
        newReq.Protocol.AfterServicesIDs.append(4837)
        newReq.Protocol.AfterServicesIDs.append(-100)
        print(newReq)
        return newReq


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
