
class DataMapper(object):
    def converter(self, response, serviceID):
        #Dispatch method
        methodName = 'service_' + str(serviceID)
        #Get the method
        method = getattr(self, methodName, lambda:'Service not existent')
        #call method
        return method(response)


    def service_624(self, response):
        return 'Dies ist ein Test String'

    def service_4885(self, response):
        return response.auto_content()

    def service_4837(self, response):
        response.to_file("test_response.mp3")
        return "Saved Audio to file"

    def service_478(self, response):
        text = ''
        for data in response.annotations["Main sentence"]:
              text = text +  data.features["prefLabel"]
        return text