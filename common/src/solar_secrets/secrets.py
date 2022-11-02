import json


class SecretKey(str, Enum):
    apiKey = "apiKey"
    dnsPassword = "dnsPassword"
    appid = "appid"


def getSecret(secretKey: SecretKey):
    secretsFilepath = f"/local/secrets.json"
    with open(secretsFilepath, "r") as secretsFile:
        secrets = json.load(secrets)

    return secrets[secretKey]
