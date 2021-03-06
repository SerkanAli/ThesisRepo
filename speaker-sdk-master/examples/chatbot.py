#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ***************************************************************************
#
#                  (C) Copyright Fraunhofer IIS 2020
#                          All Rights Reserved
#
#   This software and/or program is protected by copyright law and
#   international treaties. Any unauthorized reproduction or distribution
#   of this software and/or program, or any portion of it, may result in
#   severe civil and criminal penalties, and will be prosecuted to the
#   maximum extent possible under law.
#
# ***************************************************************************
from getpass import getpass
from pathlib import Path
from pprint import pformat, pprint
from typing import Optional, Text, Union

import click
import grpc
import sys
from google.protobuf.json_format import MessageToDict
from keycloak_login import KeyCloak, PersistentAccessToken
from speaker_sdk.speaker_pb2 import DialogueRequest
from speaker_sdk.speaker_pb2_grpc import DialogueManagerStub

DEFAULT_HOST = "api.speaker-plattform.de"
DEFAULT_AUTH_HOST = "https://www.speaker-plattform.de"


@click.command()
@click.option(
    "--host",
    default=DEFAULT_HOST,
    show_default=True,
    help="Hostname of the dialogue manager service",
)
@click.option(
    "--jwt-file",
    default=Path("certs", "login_data.json"),
    type=click.Path(),
    help="Specify file containing a valid JWT token.",
)
@click.option(
    "-u",
    "--username",
    default=None,
    type=str,
    help="Username for authentication via KeyCloak",
)
@click.option(
    "-p",
    "--password",
    default=None,
    type=str,
    help="Password for authentication via KeyCloak. User will be prompted if --user flag was provided but --password was not.",
)
@click.option(
    "--insecure", is_flag=True, help="Use insecure (unencrypted) outgoing connections",
)
@click.option(
    "--auth-host",
    default=DEFAULT_AUTH_HOST,
    type=str,
    help="Host of the authentication server.",
)
@click.option(
    "--cert",
    type=str,
    default=None,
    show_default=True,
    help="Location of certificate file",
)
@click.option(
    "--namespace", default=None, type=str, help="Namespace used for direct routing."
)
@click.option(
    "--service",
    default=None,
    type=str,
    help="Name of the service used for direct routing.",
)
@click.option("--port", default="80", type=str, help="Port used for direct routing.")
@click.option("--debug", is_flag=True, help="Request debug information from service")
def run(
    host: Text,
    jwt_file: Text,
    username: Text,
    password: Text,
    insecure: bool,
    auth_host: str,
    cert: Optional[Text],
    namespace: Text,
    service: Text,
    port: Text,
    debug: bool,
) -> None:
    """
    Prompts the user to input a textual query and subsequently calls the dialogue manager to
    process the query. The response is then printed out as well as any events sent along with it.

    With each program invocation also a new dialogue is started. During a program run, the dialogue
    tracker is carried along, i.e. the dialogue manager is provided the whole history until the
    recent turn.
    """
    tracker = None

    print(f"Connecting to {host}")

    if insecure:
        grpc_channel = grpc.insecure_channel(host)
    else:
        if cert:
            with open(cert, "rb") as f:
                creds = grpc.ssl_channel_credentials(f.read())
        else:
            creds = grpc.ssl_channel_credentials()

        grpc_channel = grpc.secure_channel(host, creds)

    if username and not password:
        password = getpass()
    keycloak = KeyCloak(auth_host=auth_host, cert=cert)
    persistent_token = PersistentAccessToken(keycloak, username, password, jwt_file)

    try:
        access_token = persistent_token.get_token()
    except Exception as e:
        print(e)
        sys.exit(1)

    print("Using access_token: %s" % access_token)

    with grpc_channel as channel:
        dm = DialogueManagerStub(channel)
        print("Enter some textual query.")

        while True:
            try:
                query = input("> ")
            except (KeyboardInterrupt, EOFError):
                break

            response = dm.handle(
                DialogueRequest(tracker=tracker, text=query, debug=debug),
                metadata=[
                    ("accesstoken", access_token),
                    ("namespace", namespace),
                    ("service", service),
                    ("port", port),
                ],
            )

            for event in response.events:
                if event.HasField("text"):
                    print(f"* Reply: {event.text}")
                elif event.HasField("event"):
                    print("* Event:", pformat(MessageToDict(event.event)))

            if response.HasField("debug_info"):
                print("#### DEBUG INFO ####")
                pprint(MessageToDict(response.debug_info))
                print("#" * 20)

            tracker = response.tracker

    print("\nBye.")


if __name__ == "__main__":
    run()
