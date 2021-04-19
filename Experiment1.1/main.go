package main

import (
	"docker_example/proto"
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

var grpcLog glog.LoggerV2

func init() {
	grpcLog = glog.NewLoggerV2(os.Stdout, os.Stdout, os.Stdout)
}

//! Server Some Comment
type Server struct {
}

//! ProccessPlainText Some Comment
func (s *Server) ProccessPlainText(ctx context.Context, msg *proto.Message) (*proto.Message, error) {
	grpcLog.Info("get msg: " + msg.Content)

	//Init Return var
	var msgout *proto.Message
	msgout = &proto.Message{}

	//Get HTTP curl link for the ELG Service
	fileELGLink, err := ioutil.ReadFile("ELGLink.txt")
	if err != nil {
		log.Fatal("No File for ELG Link!")
		msgout.Content = "No File for ELG Link"
		return msgout, nil
	}
	var sELGLink = string(fileELGLink)
	grpcLog.Info(sELGLink)

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

	grpcLog.Info("Request do...")
	resp, err := http.DefaultClient.Do(req)
	//	resp.Header.Set("Content-Type", "audio/mp3")
	if err != nil {
		// handle err
		log.Fatal(err)
	}
	grpcLog.Info("Request done Sucess!")
	if resp.StatusCode == http.StatusOK {
		bodyBytes, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatal(err)
		}
		bodyString := string(bodyBytes)
		grpcLog.Info("Response: ", bodyString)
		msgout.Content = bodyString
	}
	grpcLog.Info("Response: ", resp.StatusCode)
	defer resp.Body.Close()

	return msgout, nil
}

func main() {

	server := &Server{}

	grpcServer := grpc.NewServer()
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("error creating the server %v", err)
	}

	grpcLog.Info("Starting server at port :8080")

	proto.RegisterELGServiceServer(grpcServer, server)
	grpcServer.Serve(listener)
	grpcLog.Info("Wait for Message 2 ")
}
