package main

import (
	"bufio"
	"docker_example/proto"
	"fmt"
	"os"

	"log"
	"sync"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
)

var client proto.ELGServiceClient
var wait *sync.WaitGroup

func init() {
	wait = &sync.WaitGroup{}
}

func main() {
	log.SetOutput(os.Stdout)
	done := make(chan int)

	conn, err := grpc.Dial("localhost:8080", grpc.WithInsecure())
	if err != nil {
		log.Fatalf("Couldnt connect to service: %v", err)
	}

	client = proto.NewELGServiceClient(conn)

	log.Println("Type your message....:")
	scanner := bufio.NewScanner(os.Stdin)
	for scanner.Scan() {
		msg := &proto.Message{
			Content: scanner.Text(),
		}

		rsp, err := client.ProccessPlainText(context.Background(), msg)
		if err != nil {
			fmt.Printf("Error Sending Message: %v", err)
			break
		}

		log.Println("Response from ELG is: ", rsp.Content)
	}

	go func() {
		wait.Wait()
		close(done)
	}()

	<-done
}
