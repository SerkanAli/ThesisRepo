package main

import (
	proto_ta "docker_example/text_to_audio/proto"
	"encoding/json"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os"
	"strings"

	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
	glog "google.golang.org/grpc/grpclog"
)

var grpcLogta glog.LoggerV2

func init() {
	grpcLogta = glog.NewLoggerV2(os.Stdout, os.Stdout, os.Stdout)
}

//! Server Some Comment
type Server_ta struct {
}

//! TextToSpeech Some Comment
func (s *Server_ta) TextToSpeech(ctx context.Context, msg *proto_ta.SegmentText) (*proto_ta.AudioSegment, error) {
	grpcLogta.Info("get msg: " + msg.String())

	//Init Return var
	var msgout *proto_ta.AudioSegment
	msgout = &proto_ta.AudioSegment{}

	//Get HTTP curl link for the ELG Service
	fileELGLink, err := ioutil.ReadFile("ELGLink.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		return msgout, nil
	}
	var sELGLink = string(fileELGLink)
	grpcLogta.Info(sELGLink)

	//Get the authendification key
	fileAuthKey, err := ioutil.ReadFile("Key.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		return msgout, nil
	}
	var sAuthKey = string(fileAuthKey)

	jsonbyte, _ := json.Marshal(msg)
	body := strings.NewReader(string(jsonbyte))
	req, err := http.NewRequest("POST", sELGLink, body)
	if err != nil {
		// handle err
	}
	req.Header.Set("Authorization", "Bearer "+sAuthKey)
	req.Header.Set("Content-Type", "text/plain")

	grpcLogta.Info("Request do...")
	resp, err := http.DefaultClient.Do(req)
	//	resp.Header.Set("Content-Type", "audio/mp3")
	if err != nil {
		// handle err
		log.Fatal(err)
	}
	grpcLogta.Info("Request done Sucess!")
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		bodyString := string(bodyBytes)
		grpcLogta.Info("Response: ", bodyString)
		json.Unmarshal([]byte(bodyString), &msgout)
	}
	grpcLogta.Info("Response: ", resp.StatusCode)
	defer resp.Body.Close()

	return msgout, nil
}

func main() {

	server := &Server_ta{}

	grpcServer := grpc.NewServer()
	listener, err := net.Listen("tcp", ":8021")
	if err != nil {
		log.Fatalf("error creating the server %v", err)
	}

	grpcLogta.Info("Starting Text-to-Audio at port :8021")

	proto_ta.RegisterAudioToSpeechServer(grpcServer, server)
	grpcServer.Serve(listener)
	grpcLogta.Info("Wait for Message 2 ")
}
