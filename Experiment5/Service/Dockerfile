FROM ubuntu:20.04

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip3 install elg


COPY ./requirements.txt /requirements.txt
COPY authJSONFile ./
COPY license-1.0.0.json modelTextoText.proto modelTextoText_pb2.py modelTextoText_pb2_grpc.py ELG_Service.py resolver.py ./

WORKDIR /
RUN pip3 install -r requirements.txt
COPY . /

ENTRYPOINT [ "python3","ELG_Service.py" ]