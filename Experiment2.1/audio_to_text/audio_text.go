package main

import (
	proto_at "docker_example/audio_to_text/proto"
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

var grpcLogat glog.LoggerV2

func init() {
	grpcLogat = glog.NewLoggerV2(os.Stdout, os.Stdout, os.Stdout)
}

//! Server Some Comment
type Server_at struct {
}

//! SpeechToText Some Comment
func (s *Server_at) SpeechToText(ctx context.Context, msg *proto_at.AudioSegment) (*proto_at.SegmentText, error) {
	grpcLogat.Info("get msg: " + msg.String())

	//Init Return var
	var msgout *proto_at.SegmentText
	msgout = &proto_at.SegmentText{}

	//Get HTTP curl link for the ELG Service
	fileELGLink, err := ioutil.ReadFile("ELGLink.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		msgout.Text = "No File for ELG Link"
		return msgout, nil
	}
	var sELGLink = string(fileELGLink)
	grpcLogat.Info(sELGLink)

	//Get the authendification key
	fileAuthKey, err := ioutil.ReadFile("Key.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		msgout.Text = "No File for ELG Link"
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

	grpcLogat.Info("Request do...")
	resp, err := http.DefaultClient.Do(req)
	//	resp.Header.Set("Content-Type", "audio/mp3")
	if err != nil {
		// handle err
		log.Fatal(err)
	}
	grpcLogat.Info("Request done Sucess!")
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		bodyString := string(bodyBytes)
		grpcLogat.Info("Response: ", bodyString)
		msgout.Text = bodyString
	}
	grpcLogat.Info("Response: ", resp.StatusCode)
	defer resp.Body.Close()

	return msgout, nil
}

func main() {

	server := &Server_at{}

	grpcServer := grpc.NewServer()
	listener, err := net.Listen("tcp", ":8022")
	if err != nil {
		log.Fatalf("error creating the server %v", err)
	}

	grpcLogat.Info("Starting Audio-to-Text at port :8022")

	proto_at.RegisterAudioToSpeechServer(grpcServer, server)
	grpcServer.Serve(listener)
	grpcLogat.Info("Wait for Message 2 ")
}
