import json
from enum import Enum
from typing import Union

class SecretKey(str, Enum):
    apiKey = "apiKey"
    dnsPassword = "dnsPassword"
    appid = "appid"


def getSecret(secretKey: SecretKey):
    secretsFilepath = f"/local/secrets.json"
    with open(secretsFilepath, "r") as secretsFile:
        secrets = json.load(secrets)

def setSecret(secretKey: SecretKey, value: str = ""):
    secretsFilepath = f"/local/secrets.json"
    if os.path.exists(secretsFilePath):
        with open(secretsFilepath, "r") as secretsFile:
            secrets = json.load(secretsFile)
    else:
        secrets = {
            SecretKey.apiKey: "",
            SecreyKey.dnsPassword: "",
        }

    secrets[key] = value

    with open(secretsFilepath, "w") as secretsFile:
        json.dump(secrets, secretsFile)

    with open(secretsFilePath, "r") as secretsFile:
        secrets = json.load(secretsFile)
    
    return secrets[key]
