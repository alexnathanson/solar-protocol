import json
from enum import StrEnum, auto
from logging import error, exception


class SecretKey(StrEnum):
    networkKey = auto()  # allows posting to /api/devices
    dnsPassword = auto() # only for the gateway to update our dns entries
    appid = auto()       # used for weather data
    dnsKey = auto()      # the HASH of this key is sent to the gateway


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


def getSecretFromGateway(secretKey: SecretKey):
    url = f"https://beta.solarpowerforartists.com/secrets.php"
    dnsKey = secrets.get(secretKey.dnsKey)
    if dnsKey == None:
        return

    data = { key: dnsKey, secret: secretKey }

    try:
        response = requests.post(url=url, data=data)
        if response.ok:
            return response.text
        else:
            error(response.text)
    except:
        error(f"Error retreiving secret from gateway")


def getSecret(secretKey: SecretKey):
    secrets = getSecrets()
    secret = secrets.get(secretKey)

    if secret is None:
        gatewaySecret = getSecretFromGateway(secretKey)
        setSecret(secretKey, gatewaySecret)
        secret = secrets.get(secretKey)

    return secret


def setSecret(secretKey: SecretKey, value: str = ""):
    secrets = getSecrets() or defaultSecrets | {secretKey: value}

    with open(secretsFilepath, "w") as secretsFile:
        json.dump(secrets, secretsFile)

    return getSecret(key)
