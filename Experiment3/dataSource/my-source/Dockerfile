FROM adoptopenjdk/openjdk8-openj9:alpine-slim

ENV CONSUL_LOCATION consul

EXPOSE 8090

RUN echo 'hosts: files mdns4_minimal [NOTFOUND=return] dns mdns4' >> /etc/nsswitch.conf

COPY target/my-source.jar  /my-source.jar

ENTRYPOINT ["java", "-jar", "/my-source.jar"]
