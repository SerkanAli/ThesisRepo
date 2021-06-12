FROM ubuntu:20.04

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip install elg


COPY ./requirements.txt /requirements.txt
COPY license-1.0.0.json databroker.proto databroker_pb2.py databroker_pb2_grpc.py ELG_Databroker.py ./

WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /

ENTRYPOINT [ "python3","ELG_Databroker.py" ]