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
import click
import requests
from getpass import getpass
from pathlib import Path
from pprint import pformat, pprint
from typing import Text
from prettytable import PrettyTable

from keycloak_login import KeyCloak

@click.command()
@click.option(
    "--host",
    default="https://service-discovery.185.128.119.217.xip.io",
    show_default=True,
    help="Hostname of the service discovery server.",
)
@click.option(
    "--jwt-file",
    default=None,
    type=click.Path(),
    help="Specify file containing a valid JWT token.",
)
@click.option(
    "-u", "--username", default=None, type=str, help="Username for authentication via KeyCloak"
)
@click.option(
    "-p",
    "--password",
    default=None,
    type=str,
    help="Password for authentication via KeyCloak. User will be prompted if --user flag was provided but --password was not.",
)
@click.option(
    "--auth_host",
    default="https://speaker-keycloak.185.128.119.217.xip.io",
    type=str,
    help="Host of the authentication server.",
)
@click.option(
    "--cert",
    type=click.Path(),
    default=Path("certs", "server.crt"),
    show_default=True,
    help="Location of certificate file",
)
def run(
    host: Text,
    jwt_file: str,
    username: str,
    password: str,
    auth_host: str,
    cert: str,
) -> None:
    """
    Prints a list of services accessible to the logged in user.
    """

    print(f"Connecting to {host}")

    access_token = ""

    if jwt_file:
        try:
            access_token = open(jwt_file).read()
        except Exception as e:
            print("Error reading jwt file: %s" % e)
    else:
        if username and not password:
            password = getpass()
        keycloak = KeyCloak(auth_host=auth_host, cert=cert)
        access_token = keycloak.login(username, password)["access_token"]

    print("Using access_token: %s" % access_token)

    request_url = f"{host}/services"
    headers = {"Authorization": f"Bearer {access_token}"}

    if cert:
        response = requests.get(request_url, headers=headers, verify=cert)
    else:
        response = requests.post(request_url, headers=headers)
    response_data = response.json()

    asr_services = [[],[],[]]
    dm_services =  [[],[]]
    tts_services =  [[],[],[]]

    for entry in response_data:
        if "component" in entry["metadata"]["labels"]:
            if entry["metadata"]["labels"]["component"] == "asr":
                asr_services[0].append(entry["metadata"]["namespace"])
                asr_services[1].append(entry["metadata"]["name"])
                asr_services[2].append(entry["metadata"]["labels"]["language"])
            elif entry["metadata"]["labels"]["component"] == "dm":
                dm_services[0].append(entry["metadata"]["namespace"])
                dm_services[1].append(entry["metadata"]["name"])
            if entry["metadata"]["labels"]["component"] == "tts":
                tts_services[0].append(entry["metadata"]["namespace"])
                tts_services[1].append(entry["metadata"]["name"])
                tts_services[2].append(entry["metadata"]["labels"]["language"])

    asr_table = PrettyTable()
    asr_table.add_column("namespace", asr_services[0])
    asr_table.add_column("service", asr_services[1])
    asr_table.add_column("language", asr_services[2])

    dm_table = PrettyTable()
    dm_table.add_column("namespace", dm_services[0])
    dm_table.add_column("service", dm_services[1])

    tts_table = PrettyTable()
    tts_table.add_column("namespace", tts_services[0])
    tts_table.add_column("service", tts_services[1])
    tts_table.add_column("language", tts_services[2])

    print("\n\n")
    print("ASR services:")
    print(asr_table)
    print("\n")
    print("DM services:")
    print(dm_table)
    print("\n")
    print("TTS services:")
    print(tts_table)

if __name__ == "__main__":
    run()
