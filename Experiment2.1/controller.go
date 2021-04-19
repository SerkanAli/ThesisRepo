package main

import (
	proto_at "docker_example/audio_to_text/proto"
	proto "docker_example/proto"
	proto_ta "docker_example/text_to_audio/proto"
	proto_tt "docker_example/text_to_text/proto"
	"fmt"
	"io"
	"log"
	"net"
	"os"
	"sync"

	context "golang.org/x/net/context"
	grpc "google.golang.org/grpc"
	glog "google.golang.org/grpc/grpclog"

	"github.com/tcolgate/mp3"
	"github.com/valyala/fastjson"
)

var service_tt proto_tt.TextToTextClient
var service_at proto_at.AudioToSpeechClient
var service_ta proto_ta.AudioToSpeechClient
var wait *sync.WaitGroup
var grpcLogcnt glog.LoggerV2

func init() {
	wait = &sync.WaitGroup{}
	grpcLogcnt = glog.NewLoggerV2(os.Stdout, os.Stdout, os.Stdout)
}

//! Server Some Comment
type Server_cnt struct {
}

func main() {
	ListentoClient()

}

func (s *Server_cnt) ProcessMsg(ctx context.Context, msg *proto.Message) (*proto.Message, error) {

	//Call Translater Eng to French at port 8020
	var frenchText = Access_Text_To_Text(msg.GetContent(), "8020")

	var p fastjson.Parser
	v, err := p.Parse(frenchText)
	if err != nil {
		log.Fatal(err)
	}
	grpcLogcnt.Info(p)
	// obtain v["ask_price"] as float64
	content := v.Get("content")
	grpcLogcnt.Info("the content is : " + string(content.GetStringBytes()))

	//Call Morphosyntactic Analysis for french at port 8021
	msg.Content = Access_Text_To_Text(frenchText, "8021")

	return msg, nil
}

func ListentoClient() {
	server := &Server_cnt{}

	grpcServer := grpc.NewServer()
	listener, err := net.Listen("tcp", ":8080")
	if err != nil {
		log.Fatalf("error creating the server %v", err)
	}

	grpcLogcnt.Info("Starting Text-to-Text at port :8080")

	proto.RegisterELGServiceServer(grpcServer, server)
	grpcServer.Serve(listener)
	grpcLogcnt.Info("Wait for Message 2 ")
}

func Access_Text_To_Text(strinput string, port string) string {
	log.SetOutput(os.Stdout)
	done := make(chan int)

	conn, err := grpc.Dial("localhost:"+port, grpc.WithInsecure())
	if err != nil {
		grpcLogcnt.Fatalf("Couldnt connect to service: %v", err)
	}

	service_tt = proto_tt.NewTextToTextClient(conn)

	msg := &proto_tt.Message{
		Content: strinput,
	}

	rsp, err := service_tt.ProccessPlainText(context.Background(), msg)
	if err != nil {
		fmt.Printf("Error Sending Message: %v", err)
	}

	grpcLogcnt.Info("Response from ELG is: ", rsp.Content)

	go func() {
		wait.Wait()
		close(done)
	}()

	<-done

	return rsp.GetContent()
}

func Access_Audio_To_Text() {
	t := 0.0

	r, err := os.Open("<mp3 file path>")
	if err != nil {
		fmt.Println(err)
		return
	}

	d := mp3.NewDecoder(r)
	var f mp3.Frame
	skipped := 0

	for {

		if err := d.Decode(&f, &skipped); err != nil {
			if err == io.EOF {
				break
			}
			fmt.Println(err)
			return
		}

		t = t + f.Duration().Seconds()
	}

	fmt.Println(t)

}

func Access_Text_To_Audio() {

}
