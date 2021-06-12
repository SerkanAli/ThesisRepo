from elg import Service
from elg import Authentication
import grpc
import json
from concurrent import futures
import time
from collections import Counter

import modelTextoText_pb2
import modelTextoText_pb2_grpc
from datamapper import DataMapper


port = 8061
ServiceIDs = []

class RunElgServiceServicer(modelTextoText_pb2_grpc.RunElgServiceServicer):
    def InitParameter(self, request,context):
        global ServiceIDs
        response = modelTextoText_pb2.ELG_Text()
        ServiceIDs = request.ServiceIDs
        print("Service ID is:", ServiceIDs)
        response.PlainText = "Everything OK"
        return response

    def RunElgService(self, request,context):
        response = modelTextoText_pb2.ELG_Text()
        CurrentServiceID = request.Protocol.AfterServicesIDs[0]
        request.Protocol.AfterServicesIDs.pop(0)
        
        for ID in request.Protocol.AfterServicesIDs :
            response.Protocol.AfterServicesIDs.append(ID)

        if CurrentServiceID == -100:
            response.PlainText = request.PlainText
            return response

        auth = Authentication.from_json('authJSONFile')
        lt = Service.from_id(CurrentServiceID,auth)
        result = lt(request.PlainText)
        print(result)
        resolve = DataMapper()
        response.PlainText = resolve.converter(result, CurrentServiceID)
        return response



#test function
def SomeTesting():
    newService = RunElgServiceServicer()
    newParam = modelTextoText_pb2.ELG_Parameter()
    newParam.ServiceIDs.append(478)
    newParam.ServiceIDs.append(4885)
    newParam.ServiceIDs.append(-100)
   # newParam.ServiceID = 515
    newService.InitParameter(newParam, 'bla')
    newReq = modelTextoText_pb2.ELG_Text()
    #newReq.PlainText = 'Impfungen können zu Nebenwirkungen und ungewollten Reaktionen führen. Auch für die schnell entwickelten Covid-Impfstoffe wird eine Liste erstellt. Darauf befindet sich auch der Covid-Arm. Experten versichern jedoch: kein Grund zur Sorge.Schmerz an der Einstichstelle ist die Nebenwirkung, die bei allen vier in der EU zugelassenen Impfstoffen am häufigsten genannt wird. Doch bei manchen bleibt es nicht dabei. Sie klagen darüber, dass der gesamte Arm so wehtut, dass man ihn kaum anheben kann. Sogar das Tippen auf der Tastatur ist problematisch. Auch von Rötungen, Schwellungen und Juckreiz rund um die Einstichstelle wird berichtet. Die Beschreibungen des Covid-Arms kommen häufiger von jungen Frauen, die mit einem mRNA-Impfstoff immunisiert worden sind - und können verunsichern.Eine Klinik-Mitarbeiterin zieht den Covid-19 Impfstoff für eine Impfung auf eine Spritze. Auch das Paul-Ehrlich-Institut (PEI) hat diese unerwünschten Wirkungen nach einer Impfung in einem Bericht aufgenommen. Darin heißt es: "Diese verzögerten Lokalreaktionen können etwa eine Woche nach der Impfung auftreten und sind gekennzeichnet durch eine in der Regel gut abgrenzbare Hautrötung und Schwellung am geimpften Arm, in einigen Fällen verbunden mit Schmerzen und/oder Juckreiz." Die Bundesbehörde für Impfstoffe führt weiter aus, dass bis zu acht Tage vergehen könnten, bis die Schmerzen im Arm ihren Höhepunkt erreichen. Zunächst war es in diesem Zusammenhang ausschließlich zu Fällen mit dem Moderna-Impfstoff gekommen, weshalb auch vom Moderna-Arm die Rede war. Nun ist klar, dass die unangenehme Wirkung auch beim Impfstoff von Biontech auftritt.'
    newReq.PlainText = 'Meistens ist der Stoff eine grünlich glasige Masse aus geschmolzenem Quarz und Feldspat. Hallo, nebensatz!. Teile der Schmelzmassen allerdings enthalten große Mengen Metalle, die aus der verdampften Infrastruktur stammen'
    newReq.Protocol.BeforeServiceID = -1
    newReq.Protocol.CurrentServiceID = -1
    newReq.Protocol.AfterServicesIDs.append(478)
    newReq.Protocol.AfterServicesIDs.append(4885)
    newReq.Protocol.AfterServicesIDs.append(-100)
    while True:
        response = newService.RunElgService(newReq, 'bla')
        newReq = response
        if Counter(response.Protocol.AfterServicesIDs) == Counter() :
            break


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








