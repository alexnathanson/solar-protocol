import json
from enum import StrEnum, auto
from logging import error, exception
import requests

filepath = "/local/secrets.json"

class SecretKey(StrEnum):
    networkkey = auto()  # allows posting to /api/devices
    dnspassword = auto()  # only for the gateway to update our dns entries
    appid = auto()  # used for weather data
    dnskey = auto()  # the HASH of this key is sent to the gateway


def getSecrets():
    try:
        with open(filepath, "r") as secretsFile:
            secrets = json.load(secretsFile)
            return secrets
    except FileNotFoundError:
        with open(filepath, "w") as secretsFile:
            json.dump({}, secretsFile)
            secrets = json.load(secretsFile)
            return secrets


def getSecretFromGateway(secretkey: SecretKey):
    url = f"https://beta.solarpowerforartists.com/secrets.php"
    dnskey = getSecret(SecretKey.dnskey)
    if dnskey == None:
        return

    data = {"key": dnskey, "secret": secretkey}

    try:
        response = requests.post(url=url, data=data)
        if response.ok:
            return response.text
        else:
            error(response.text)
    except:
        error(f"Error retreiving secret from gateway")


def getSecret(key: SecretKey):
    secrets = getSecrets()
    secret = secrets.get(key)
    if secret is not None:
        return secret

    if key not in [ SecretKey.appid, SecretKey.networkkey ]:
     return secret

    try:
        gatewaySecret = getSecretFromGateway(key)
        if gatewaySecret is not None:
            return setSecret(key, gatewaySecret)
    except:
        pass


def setSecret(key: SecretKey, value: str = ""):
    secrets = getSecrets() | {key: value}

    with open(filepath, "w") as secretsFile:
        json.dump(secrets, secretsFile)

    return getSecret(key)
