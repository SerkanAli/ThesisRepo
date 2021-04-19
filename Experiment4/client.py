import grpc



#from Databroker import clientData
from Parameter import clientParameter
#from Service import clientService
from google.protobuf import empty_pb2

#speak first of all to the databroker
#response_DataBroker = clientData.RunDatabroker()
#print('Databroker response is:', response_DataBroker)




#with the data of the databroker and parameter, next speak to the elg service model
#response_Service = clientService.RunService(response_DataBroker.PlainText, response_Parameter.ServiceID)



class TestClient:
    def __init__(self):
        self.test = None

    @classmethod
    def RunServices(self):
        #then to the parameter
        response_Parameter = clientParameter.RunParameter()
        print('Parameter response is:', response_Parameter)
        #response_Service = clientService.RunService("Hello World", 473)
        #print('Service Response:', response_Service)
        return response_Parameter

