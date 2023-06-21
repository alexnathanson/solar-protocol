"""
Every server runs this script
This collects the photovoltaic data from remote servers via api/charge-controller 
The purpose of this is minimize the amount of on the fly API calls
"""

import os
import requests
import sys
from logging import exception, info

os.chdir(sys.path[0])  # if this script is called from a different directory


def run():
    info("***** Running GET Remote Data script *****")

    # initialize SolarProtocolClass
    solarProtocol = SolarProtocolClass()

    ips = solarProtocol.getDeviceValues("ip")
    names = solarProtocol.getDeviceValues("name")

    for ip, name in zip(ips, names):
        info(f"{name}: {ip}")

        url = f"http://{ip}/api/charge-controller"
        params = {"days": 4}

        try:
            response = requests.get(url=url, params=params)
        except requests.exceptions.HTTPError:
            exception("HTTP Error")
        except requests.exceptions.Timeout:
            exception("Timeout")
        except Exception:
            exception("Unknown Error")

        if response.status_code == 200:
            info("GET request successful")

        filename = name.replace(" ", "-").lower()
        with open(f"/data/devices/{filename}.json", "w", encoding="utf-8") as file:
            file.write(response.text)
            file.close()


# FIXME: explain why one imports with . prefix and the other does not
if __name__ == "__main__":
    from SolarProtocolClass import SolarProtocol as SolarProtocolClass
    import logging

    LOGLEVEL = os.environ.get("LOGLEVEL", "WARNING").upper()
    logging.basicConfig(level=LOGLEVEL)
    print(f"{LOGLEVEL=}")

    run()
else:
    from .SolarProtocolClass import SolarProtocol as SolarProtocolClass
