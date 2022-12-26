import json
from enum import StrEnum, auto
from logging import error

class SecretKey(StrEnum):
    apiKey = auto()
    dnsPassword = auto()
    appid = auto()


defaultSecrets = {
    SecretKey.apiKey: "",
    SecretKey.dnsPassword: "",
    SecretKey.appid: "",
}


def getSecrets(filepath="/local/secrets.json"):
    try:
        with open(filepath, "r") as secretsFile:
            return json.load(filepath)
    except FileNotFoundError:
        error(f"Missing {filepath}, please create one!")


def getSecret(secretKey: SecretKey):
    secrets = getSecrets()
    default = defaultSecrets.get(secretKey)
    return secrets.get(secretKey, default)


def setSecret(secretKey: SecretKey, value: str = ""):
    secrets = getSecrets() or defaultSecrets | {secretKey: value}

    with open(secretsFilepath, "w") as secretsFile:
        json.dump(secrets, secretsFile)

    return getSecret(key)
