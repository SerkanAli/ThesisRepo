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
from typing import Dict

import click
import requests
import jwt
import json
import time
from pathlib import Path
from typing import Optional, Text, Union


class KeyCloak:
    def __init__(
        self,
        auth_host: Text,
        realm: Text = "Speaker",
        client_id: Text = "speaker-platform",
        cert: Optional[Text] = None,
    ):
        self.auth_host = auth_host
        self.realm = realm
        self.client_id = client_id
        self.cert = cert
        self.token_url = (
            f"{auth_host}/auth/realms/{realm}/protocol/openid-connect/token"
        )

    def login(
        self, username: Text = None, password: str = None, refresh_token: str = None
    ) -> Dict:

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = (
            {
                "grant_type": "refresh_token",
                "client_id": self.client_id,
                "refresh_token": refresh_token,
            }
            if refresh_token
            else {
                "grant_type": "password",
                "client_id": self.client_id,
                "username": username,
                "password": password,
            }
        )

        if self.cert:
            response = requests.post(
                self.token_url, data=data, headers=headers, verify=self.cert
            )
        else:
            response = requests.post(
                self.token_url, data=data, headers=headers, verify=True
            )
        response_data = response.json()

        if "error" in response_data:
            raise Exception(
                response_data.get("error_description") or response_data.get("error")
            )
        return response_data


class PersistentAccessToken:
    """
    Persists the login data from Keycloak (`self.login_data`) as a json file (`self.filename`).
    The user only needs to call the method `self.get_token()`, which will retrieve the token from the
    file and check whether it's still valid, renewing it with the refresh token if not.
    """

    def __init__(
        self, keycloak: KeyCloak, username: str, password: str, filename: Path,
    ):
        self.keycloak = keycloak
        self.username = username
        self.password = password
        self.filename = filename
        self.login_data = {}

    def _refresh_login_data(self) -> None:
        """
        Gets a new token from the Keycloak server and writes it to `self.filename`.
        """
        # If username and password are provided, just get a new token
        # regardless of whether there's login_data already
        if self.username and self.password:
            print("Getting new token from Keycloak server")
            self.login_data = self.keycloak.login(
                username=self.username, password=self.password
            )
        elif self.login_data:
            if self.is_expired(self.login_data["access_token"]):
                if self.is_expired(self.login_data["refresh_token"]):
                    raise Exception(
                        "Your access and refresh tokens have expired. Please log in again."
                    )
                else:
                    print(
                        "Your access token has expired. Using refresh token to get a new one."
                    )
                    self.login_data = self.keycloak.login(
                        refresh_token=self.login_data["refresh_token"]
                    )
            else:
                print("Reusing access token found in %s" % self.filename)
        else:
            raise Exception(
                "No access token found. Please log in for the first time so your login data gets saved."
            )

        self._dump_login_data()

    def _dump_login_data(self) -> None:
        """
        Writes the login data to `self.filename`, creating the file if it doesn't exist.
        """
        with open(self.filename, "w") as fout:
            json.dump(self.login_data, fout, indent=2)

    def _load_login_data(self) -> None:
        """
        Reads the login data from `self.filename`
        """
        try:
            with open(self.filename, "r") as fin:
                self.login_data = json.load(fin)
        except FileNotFoundError as e:
            # Ignore. We'll populate it when we call _refresh_login_data()
            self.login_data = {}

    def is_expired(self, token: str) -> bool:
        """Compare the `exp` claim of `token` against the current time (UTC).

        Args:
            token (str): a JSON Web Token

        Returns:
            bool: True if the token is expired, False otherwise
        """

        decoded_token = jwt.decode(
            token, options={"verify_signature": False}, algorithms=["R256", "HS256"]
        )
        return decoded_token["exp"] < time.time()

    def get_token(self) -> str:
        """This is the only method the user needs to get a valid token on every call.
        Loads the login data from `self.filename` onto `self.login_data` and refreshes
        the tokens if necessary.

        Returns:
            str: a valid JSON Web Token
        """
        self._load_login_data()
        self._refresh_login_data()
        return self.login_data["access_token"]


@click.command()
@click.option(
    "-u",
    "--username",
    default=None,
    required=True,
    type=str,
    help="Username for authentication via KeyCloak",
)
@click.option(
    "-p",
    "--password",
    default=None,
    prompt=True,
    hide_input=True,
    type=str,
    help="Password for authentication via KeyCloak. User will be prompted if not provided.",
)
@click.option(
    "--auth-host",
    default="https://www.speaker-plattform.de",
    type=str,
    help="Host of the authentication server.",
)
@click.option(
    "--cert",
    type=str,
    default=None,
    show_default=False,
    help="Location of certificate file",
)
@click.option(
    "--token-file",
    type=click.Path(),
    default=Path("certs", "login_data.json"),
    show_default=True,
    help="Location of token file",
)
def fetch_token(
    username: Text,
    password: Text,
    auth_host: Text,
    cert: click.Path(),
    token_file: click.Path(),
):
    keycloak = KeyCloak(auth_host=auth_host, cert=cert)
    persistent_token = PersistentAccessToken(keycloak, username, password, token_file)
    token = persistent_token.get_token()

    print(f"User JWT:\n{token}")


if __name__ == "__main__":
    fetch_token()
