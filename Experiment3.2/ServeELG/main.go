package main

import (
	"io/ioutil"
	"log"
	"net/http"

	"encoding/csv"
	"fmt"
	"os"
)

//holds infomartion about specific ELG service
type ELGService struct {
	ServiceName string
	ServiceLink string
	ServiceKey  string
}

//map structure to fast lookup for all ELG services
var allELGServices map[string]ELGService

func apiResponse(w http.ResponseWriter, r *http.Request) {
	//Reached here, therefore status is OK
	w.WriteHeader(http.StatusOK)

	//Read reuest body
	body, err := ioutil.ReadAll(r.Body)
	if err != nil {
		log.Printf("Error reading body: %v", err)
		http.Error(w, "can't read body", http.StatusBadRequest)
		return
	}
	param := string(body)
	log.Printf(param)
	//check if the given request name is inside dataset
	bufService, check := allELGServices[param]

	if check == false {
		log.Printf("Param is invalid")
		http.Error(w, "The given request param is false", http.StatusBadRequest)
		return
	}

	//when everything is ok, then assing link and key of the ELG service into the response
	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(`{"ELG_ServiceLink":"` + bufService.ServiceLink + `" , "ELG_Key":"` + bufService.ServiceKey + `"}`))

}

//this functions load all data, which is here saved as csv file
func readAllServices() {
	csvFile, err := os.Open("elg.csv")
	if err != nil {
		fmt.Println(err)
	}
	fmt.Println("Successfully Opened CSV file")
	defer csvFile.Close()

	csvLines, err := csv.NewReader(csvFile).ReadAll()
	if err != nil {
		fmt.Println(err)
	}
	allELGServices = make(map[string]ELGService)
	for _, line := range csvLines {
		emp := ELGService{
			ServiceName: line[0],
			ServiceLink: line[1],
			ServiceKey:  line[2],
		}
		allELGServices[emp.ServiceName] = emp
	}

}

func main() {
	readAllServices()
	log.Printf(allELGServices["tildeende"].ServiceLink)
	http.HandleFunc("/", apiResponse)
	log.Fatal(http.ListenAndServe("localhost:8150", nil))
}
