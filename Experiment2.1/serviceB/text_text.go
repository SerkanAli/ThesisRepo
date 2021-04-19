package main

import (
	proto_tt "docker_example/text_to_text/proto"
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

var grpcLogtt glog.LoggerV2

func init() {
	grpcLogtt = glog.NewLoggerV2(os.Stdout, os.Stdout, os.Stdout)
}

//! Server Some Comment
type Server_tt struct {
}

//! ProccessPlainText Some Comment
func (s *Server_tt) ProccessPlainText(ctx context.Context, msg *proto_tt.Message) (*proto_tt.Message, error) {
	grpcLogtt.Info("get msg: " + msg.Content)

	//Init Return var
	var msgout *proto_tt.Message
	msgout = &proto_tt.Message{}

	//Get HTTP curl link for the ELG Service
	fileELGLink, err := ioutil.ReadFile("ELGLink.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		msgout.Content = "No File for ELG Link"
		return msgout, nil
	}
	var sELGLink = string(fileELGLink)

	//Get the authendification key
	fileAuthKey, err := ioutil.ReadFile("Key.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		msgout.Content = "No File for ELG Link"
		return msgout, nil
	}
	var sAuthKey = string(fileAuthKey)

	body := strings.NewReader(msg.Content)
	req, err := http.NewRequest("POST", sELGLink, body)
	if err != nil {
		// handle err
	}
	req.Header.Set("Authorization", "Bearer "+sAuthKey)
	req.Header.Set("Content-Type", "text/plain")

	grpcLogtt.Info("Request to...")
	grpcLogtt.Info(sELGLink)
	resp, err := http.DefaultClient.Do(req)
	//	resp.Header.Set("Content-Type", "audio/mp3")
	if err != nil {
		// handle err
		log.Fatal(err)
	}
	grpcLogtt.Info("Request done Sucess!")
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		bodyString := string(bodyBytes)
		grpcLogtt.Info("Response: ", bodyString)
		msgout.Content = bodyString
	}
	grpcLogtt.Info("Response: ", resp.StatusCode)
	defer resp.Body.Close()

	return msgout, nil
}

func main() {

	server := &Server_tt{}

	grpcServer := grpc.NewServer()
	listener, err := net.Listen("tcp", ":8021")
	if err != nil {
		log.Fatalf("error creating the server %v", err)
	}

	grpcLogtt.Info("Starting Text-to-Text at port :8021")

	proto_tt.RegisterTextToTextServer(grpcServer, server)
	grpcServer.Serve(listener)
	grpcLogtt.Info("Wait for Message 2 ")
}
