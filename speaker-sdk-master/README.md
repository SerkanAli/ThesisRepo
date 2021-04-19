# Speaker SDK

Welcome to the Speaker Software Development Kit (SDK).

## Interface Specification

You may find the gRPC and Protobuf specification here: [Interfaces](interfaces.md)

### gRPC

The platform offers all its services over a gRPC API which is a combination of a technique called Remote Procedure Calls (RPC) and the modern HTTP/2.0 protocol for efficient bi-directional streamable communication.

> gRPC is a modern open source high performance RPC framework that can run in any environment. It can efficiently connect services in and across data centers with pluggable support for load balancing, tracing, health checking and authentication. It is also applicable in last mile of distributed computing to connect devices, mobile applications and browsers to backend services.

Source: [grpc.io](https://grpc.io/about/)

### WebSockets

We will also provide a [WebSocket](https://tools.ietf.org/html/rfc6455) interface which will provide the same services and behaviour as the gRPC interface.
In addition, all messages will be sent and received in JSON format instead of the binary Protobuf format.

*Note:* We generally recommend using the gRPC interface, but provide this WebSocket interface for connecting with web clients.

## Examples

### Preparation

Create a virtual environment and install the required packages:

```shell
cd examples

python3.7 -m venv .env
source .env/bin/activate        # Windows: source .env/Scripts/activate
pip install -r requirements.txt
```

### Run

#### Server

There is a `server_mockup.py` which implements a gRPC server and provides interfaces to mockups of these three services. If they are called, e.g. from a client, they adhere to the interface specification and behave like described but only produce dummy results.

You can start this server locally to check out the client examples below.

```shell
python server_mockup.py
```

#### Clients

In the directory `/examples` are minimalistic client implementations in Python which show how to access the three services (speech recognition, dialogue manager, and text to speech) directly.

```shell
python speech_recognition.py --insecure
python chatbot.py --insecure
python text_to_speech.py --insecure
```

Calling the clients with the parameter `--insecure` will assume that a server is running at `localhost:50000`, which is also the default setting for the `server_mockup.py`. You can change the hostname of the server or a few other parameters, like samplerate, language or audio encoding, using the command line parameters. By invoking each of the clients with the parameter `--help` they will print a list of supported parameters and their respective description and default value.

```shell
python speech_recognition.py --help
```

#### Accessing the speaker cluster

---

## <span style="color: red">ATTENTION: NOTES ON PRIVACY AND DATA SECURITY</span>

We care for your privacy and the security of your data. Thus, we want to be fully transparent with you at any time about the current capabilities and limitations of the SPEAKER platform. The following section will try to answer some questions you might have. It will be constantly updated during the project. Please read it carefully before accessing the platform.

* **Is my connection encrypted?**\
We use TLS termination at ingress level (an ingress is basically a reverse proxy at the edge of Kubernetes). This means your connection is **encrypted from the client to the edge of the cluster**. Communication **INSIDE the cluster** itself is **NOT encrypted**. According to the documentation of ingress-nginx (https://kubernetes.github.io/ingress-nginx/user-guide/tls/) it uses TLS 1.2 and 1.3. As we do not have an official domain and certificate yet, we have to use a self-signed certificate which you can find in examples/certs. The certificate belongs to a 2048-bit RSA key pair generated with openssl.

* **How is authorization handled and can other people access my services?**\
In the current phase, only generic services are deployed to the cluster which are accessible by all partners via the same **JSON web token**. As the project progresses, a sophisticated user management will be established and partner-specific services will be deployed. At that point in time each partner will receive a specific token which will grant them access solely to the services they are entitled to use.

* **Is my data stored on the cluster?**\
At the ingress controller, a **default access log** is printed to stdout and stderr which includes a **timestamp**, the **IP** address of the user and the **endpoint** to which the request is routed. Concerning our own services (API Gateway, KWS, ASR & TTS), the current versions which we provide on the cluster are designed to be stateless. **We do not store any data persistently** and when a service (or "pod" in Kubernetes terms) is destroyed, all (transient) data associated to it is lost. **HOWEVER**, in the current pilot phase, services are deployed with **debug logs** which **are written to stdout and stderr** which include transcripts from the ASR and text input for the TTS. Although **we do not store those logs**, it is possible for a person with **privileged administrative access rights** to the Kubernetes cluster to **access** and **read** them.

* **Who has privileged administrative access rights?**\
Currently five individuals from the Fraunhofer SPEAKER team and our cloud provider Cloud & Heat have priviledged administrative access to the cluster. The access is granted via a special access token (a so called "kubeconfig") and is further secured by a VPN (WireGuard).

---

To access the speaker cluster a valid JSON web token is required. A token can be obtained by logging in into our authentication server with the username and password provided to you via E-Mail. Simply use the following command:

```sh
python keycloak_login.py -u <your_username>
```

This will prompt you to enter your password. If the login is successful, a token is printed to the stdout which is valid for seven days. Simply copy the token into a file for later use. In the following instructions we assume you copied it to `examples/certs/jwt`.

Use the following commands to access the speaker cluster:

```bash

# TTS synthesizing a default text ("Hello, I'm a virtual assistant.")
python text_to_speech.py --host api-speaker.185.128.119.217.xip.io --jwt-file certs/jwt

# TTS synthesizing a specific text
python text_to_speech.py --host api-speaker.185.128.119.217.xip.io --jwt-file certs/jwt "hello, how do you do?"

# ASR
python speech_recognition.py --host api-speaker.185.128.119.217.xip.io --jwt-file certs/jwt

# DM (example deployment, only echos back what was received)
python chatbot.py --host api-speaker.185.128.119.217.xip.io --jwt-file certs/jwt

```

### Further notes

#### Login

Aside from using the JSON web token directly you can also access the services via the option `-u <your_username>` with your credentials.

#### Language Selection

It is possible to switch the language for the ASR and the TTS. This can be done by additionally providing the command line parameter `--language` with a valid language code (currently supported: `en-US` and `de-DE`).

#### Accessing Specialized Services

Some partners have access to specialized services. To use them on the Speaker Cluster, first check the services available to you. This can be done with this command:

```sh
python list_services.py --host https://service-discovery.185.128.119.217.xip.io --jwt-file certs/jwt_tmp

# alternative:
python list_services.py --host https://service-discovery.185.128.119.217.xip.io -u <your_username>
```

The script will print three tables (one for each service type - ASR, DM, TTS) to stdout, which might look similar to this:

```sh
ASR services:
+--------------+---------------------+----------+
|  namespace   |       service       | language |
+--------------+---------------------+----------+
|   speaker    |    speaker-asr-de   |  de-DE   |
|   speaker    |    speaker-asr-en   |  en-US   |
| demonstrator | demonstrator-asr-de |  de-DE   |
| demonstrator | demonstrator-asr-en |  en-US   |
+--------------+---------------------+----------+

DM services:
+--------------+------------+
|  namespace   |  service   |
+--------------+------------+
|   speaker    | speaker-dm |
| demonstrator |   dm-en    |
+--------------+------------+

TTS services:
+--------------+---------------------+----------+
|  namespace   |       service       | language |
+--------------+---------------------+----------+
|   speaker    |    speaker-tts-de   |  de-DE   |
|   speaker    |    speaker-tts-en   |  en-US   |
| demonstrator | demonstrator-tts-de |  de-DE   |
+--------------+---------------------+----------+
```

You will see a set of services (with their eligible language options) belonging to different namespaces. In the current setup, generic services available to all partners are deployed into the `speaker` namespace. Specialized services are deployed into separate namespaces which are only available to the respective partners.

To access those services, the `api-gateway` and the `example clients` where extended to make it possible to directly route to the respective service by providing it's name and the namespace it's deployed in. Based on the list of services above, you could for example access different dialog managers using the `--namespace` and `--service` parameters:

```sh
# accessing speaker/speaker-dm
python chatbot.py --host api-speaker.185.128.119.217.xip.io --jwt-file certs/jwt --namespace speaker --service speaker-dm

# accessing demonstrator/dm-en
python chatbot.py --host api-speaker.185.128.119.217.xip.io --jwt-file certs/jwt --namespace demonstrator --service dm-en
```