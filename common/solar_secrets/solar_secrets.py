import json
from enum import Enum

secretsFilepath = f"/local/secrets.json"

defaultSecrets = {
    SecretKey.apiKey: "",
    SecreyKey.dnsPassword: "",
    SecreyKey.appid: "",
}

class SecretKey(str, Enum):
    apiKey = "apiKey"
    dnsPassword = "dnsPassword"
    appid = "appid"

def getSecrets():
    with open(secretsFilepath, "r") as secretsFile:
        return json.load(secrets)


def getSecret(secretKey: SecretKey):
    secrets = getSecrets() or defaultSecrets
    return secrets[secretKey]


def setSecret(secretKey: SecretKey, value: str = ""):
    secrets = getSecrets() or defaultSecrets | { secretKey: value }

    with open(secretsFilepath, "w") as secretsFilepath:
        json.dump(secrets, secretsFilepath)

    return getSecret(key)
