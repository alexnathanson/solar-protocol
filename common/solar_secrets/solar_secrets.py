import json
from enum import Enum

secretsFilepath = f"/local/secrets.json"

class SecretKey(str, Enum):
    apiKey = "apiKey"
    dnsPassword = "dnsPassword"
    appid = "appid"

defaultSecrets = {
    SecretKey.apiKey: "",
    SecretKey.dnsPassword: "",
    SecretKey.appid: "",
}

def getSecrets():
    with open(secretsFilepath, "r") as secretsFile:
        return json.load(secretsFile)


def getSecret(secretKey: SecretKey):
    secrets = getSecrets() or defaultSecrets
    return secrets[secretKey]


def setSecret(secretKey: SecretKey, value: str = ""):
    secrets = getSecrets() or defaultSecrets | { secretKey: value }

    with open(secretsFilepath, "w") as secretsFile:
        json.dump(secrets, secretsFile)

    return getSecret(key)
