from hashlib import new
import grpc
import modelTextoText_pb2
import modelTextoText_pb2_grpc
from google.protobuf import empty_pb2
from collections import Counter


def RunServiceWithParameter(PlainText, ServiceID):
    port_Service = 'localhost:8061'
    channel_Service = grpc.insecure_channel(port_Service)
    stub_Service = modelTextoText_pb2_grpc.RunElgServiceStub(channel_Service)

    newParam = modelTextoText_pb2.ELG_Parameter()
    newParam.ServiceIDs.append(478)
    newParam.ServiceIDs.append(4885)
    newParam.ServiceIDs.append(4837)
   # newParam.ServiceID = 515
    stub_Service.InitParameter(newParam)
    newReq = modelTextoText_pb2.ELG_Text()
    #newReq.PlainText = 'Impfungen können zu Nebenwirkungen und ungewollten Reaktionen führen. Auch für die schnell entwickelten Covid-Impfstoffe wird eine Liste erstellt. Darauf befindet sich auch der Covid-Arm. Experten versichern jedoch: kein Grund zur Sorge.Schmerz an der Einstichstelle ist die Nebenwirkung, die bei allen vier in der EU zugelassenen Impfstoffen am häufigsten genannt wird. Doch bei manchen bleibt es nicht dabei. Sie klagen darüber, dass der gesamte Arm so wehtut, dass man ihn kaum anheben kann. Sogar das Tippen auf der Tastatur ist problematisch. Auch von Rötungen, Schwellungen und Juckreiz rund um die Einstichstelle wird berichtet. Die Beschreibungen des Covid-Arms kommen häufiger von jungen Frauen, die mit einem mRNA-Impfstoff immunisiert worden sind - und können verunsichern.Eine Klinik-Mitarbeiterin zieht den Covid-19 Impfstoff für eine Impfung auf eine Spritze. Auch das Paul-Ehrlich-Institut (PEI) hat diese unerwünschten Wirkungen nach einer Impfung in einem Bericht aufgenommen. Darin heißt es: "Diese verzögerten Lokalreaktionen können etwa eine Woche nach der Impfung auftreten und sind gekennzeichnet durch eine in der Regel gut abgrenzbare Hautrötung und Schwellung am geimpften Arm, in einigen Fällen verbunden mit Schmerzen und/oder Juckreiz." Die Bundesbehörde für Impfstoffe führt weiter aus, dass bis zu acht Tage vergehen könnten, bis die Schmerzen im Arm ihren Höhepunkt erreichen. Zunächst war es in diesem Zusammenhang ausschließlich zu Fällen mit dem Moderna-Impfstoff gekommen, weshalb auch vom Moderna-Arm die Rede war. Nun ist klar, dass die unangenehme Wirkung auch beim Impfstoff von Biontech auftritt.'
    newReq.PlainText = 'Meistens ist der Stoff eine grünlich glasige Masse aus geschmolzenem Quarz und Feldspat. Hallo, nebensatz!. Teile der Schmelzmassen allerdings enthalten große Mengen Metalle, die aus der verdampften Infrastruktur stammen'
    newReq.Protocol.BeforeServiceID = -1
    newReq.Protocol.CurrentServiceID = -1
    newReq.Protocol.AfterServicesIDs.append(478)
    newReq.Protocol.AfterServicesIDs.append(4885)
    newReq.Protocol.AfterServicesIDs.append(4837)
    while True:
        response = stub_Service.RunElgService(newReq)
        newReq = response
        if Counter(response.Protocol.AfterServicesIDs) == Counter() :
            break
    return newReq
    


RunServiceWithParameter('How about today?', -1) 