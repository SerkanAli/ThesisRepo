from typing import Dict

import click
import requests
from pathlib import Path

class KeyCloak:
    def __init__(
        self,
        auth_host: str = "https://speaker-keycloak.185.128.119.217.xip.io",
        realm: str = "Speaker",
        client_id: str = "speaker-platform",
        cert: str = ""
    ):
        self.auth_host = auth_host
        self.realm = realm
        self.client_id = client_id
        self.cert = cert
        self.token_url = f"{auth_host}/auth/realms/{realm}/protocol/openid-connect/token"

    def login(self, username: str, password: str) -> Dict:

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": username,
            "password": password,
            "grant_type": "password",
            "client_id": self.client_id,
        }

        if self.cert:
            response = requests.post(self.token_url, data=data, headers=headers, verify=self.cert)
        else:
            response = requests.post(self.token_url, data=data, headers=headers)
        response_data = response.json()

        if "error" in response_data:
            raise Exception(response_data["error_description"])
        return response_data


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
def fetch_token(username: str, password: str, auth_host: str, cert: click.Path()):
    keycloak = KeyCloak(auth_host=auth_host, cert=cert)
    token = keycloak.login(username, password)
    print(f"User JWT:\n{token['access_token']}")


if __name__ == "__main__":
    fetch_token()
