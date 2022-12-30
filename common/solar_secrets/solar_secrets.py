import json
from enum import StrEnum, auto
from logging import error, exception


class SecretKey(StrEnum):
    networkkey = auto()  # allows posting to /api/devices
    dnspassword = auto() # only for the gateway to update our dns entries
    appid = auto()       # used for weather data
    dnskey = auto()      # the HASH of this key is sent to the gateway


def getSecrets(filepath="/local/secrets.json"):
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
    dnskey = getSecrets(SecretKey.dnskey)
    if dnskey == None:
        return

    data = { key: dnskey, secret: secretkey }

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

    if secret is None:
        gatewaySecret = getSecretFromGateway(key)
        setSecret(key, gatewaySecret)
        secret = secrets.get(key)

    return secret


def setSecret(key: SecretKey, value: str = ""):
    secrets = getSecrets() or defaultSecrets | {key: value}

    with open(secretsFilepath, "w") as secretsFile:
        json.dump(secrets, secretsFile)

    return getSecret(key)
