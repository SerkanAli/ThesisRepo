FROM ubuntu:20.04

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip install elg


COPY ./requirements.txt /requirements.txt
COPY authJSONFile ./
COPY license-1.0.0.json modelAudioToText.proto modelAudioToText_pb2.py modelAudioToText_pb2_grpc.py ELG_ServiceAT.py ./

WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /

ENTRYPOINT [ "python3","ELG_ServiceAT.py" ]