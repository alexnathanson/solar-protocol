import csv
import datetime
import json
import os
import sys

from enum import Enum
from typing import Union

from fastapi import FastAPI, Header, Form

import requests

# header for datalogger csv
fieldnames = [
    "timestamp",
    "PV voltage",
    "PV current",
    "PV power L",
    "PV power H",
    "battery voltage",
    "battery current",
    "battery power L",
    "battery power H",
    "load voltage",
    "load current",
    "load power",
    "battery percentage",
]

# safelist of keys we can share from local.json
safe_keys = [
    "color",
    "name",
    "description",
    "location",
    "city",
    "country",
    "pvWatts",
    "pvVolts"
]

class ChargeKeys(str, Enum):
    PV_voltage = "PV voltage"
    PV_current = "PV current"
    PV_power_L = "PV power L"
    PV_power_H = "PV power H"
    battery_voltage = "battery voltage"
    battery_current = "battery current"
    battery_power_L = "battery power L"
    battery_power_H = "battery power H"
    load_voltage = "load voltage"
    load_current = "load current"
    load_power = "load power"
    battery_percentage = "battery percentage"
    scaled_wattage = "scaled wattage"


class SystemKeys(str, Enum):
    tz = "tz"
    color = "color"
    description = "description"
    name = "name"
    location = "location"
    city = "city"
    country = "country"
    pvWatts = "pvWatts"
    pvVolts = "pvVolts"


app = FastAPI(title="solar-protocol", docs_url="/api/docs")

def getTimezone():
    return os.environ['TZ'] if "TZ" in os.environ else "America/New_York"

def getWattageScale():
    pvWatts = getLocal("pvWatts")
    if pvWatts != None and pvWatts != "":
        return 50.0 / float(pvWatts)

    return 1

@app.get("/api")
def root():
    return {"message": "Hello World 👋"}

class DeviceKeys(str, Enum):
    tz = "tz"
    name = "name"
    log = "log"
    timestamp = "timestamp"

@app.get("/api/status")
def devices():
    response = requests("/status")
    status = response.text.split("\n")
    stats = status[2]
    [accepts, handled, reqs] = status.split(' ')

    return {
            "uptime": "todo",
            "rps": "todo",
            "accepts": accepts,
            "handled": handled,
            "requests": reqs,
            "cpu load": "todo",
    }

@app.get("/api/devices")
def devices(key: Union[DeviceKeys, None] = None):
    filename = f"/data/devices.json"

    with open(filename, "r") as jsonfile:
        devices = json.load(jsonfile)

    if key == None:
        return [{ key: device[key] for key in DeviceKeys } for device in devices]

    return [{ key: device[key] } for device in devices]


@app.get("/api/system")
def system(key: Union[SystemKeys, None] = None):
    if key == SystemKeys.tz:
        return getTimezone()

    return getLocal(key)

@app.get("/api/charge/{day}")
def getChargeForDay(day: str, key: Union[ChargeKeys, None] = None):
    return charge(days=[day], key=key)

@app.get("/api/charge")
def getCharge(days: Union[int, None] = None, key: Union[ChargeKeys, None] = None):
    today = datetime.date.today()

    if days == None:
        return charge(days, key=key)

    return charge(days=[ today - datetime.timedelta(days=days) for days in range(days)], key=key)

def charge(days: Union[list[str], None] = None, key: Union[ChargeKeys, None] = None):
    filepath = "/data/traces"

    rows = []
    if days == None:
        dates = [ datetime.date.today() ]
    else:
        dates = days

    for date in dates:
        try:
            with open(f"{filepath}/{date}.csv", "r") as csvfile:
                reader = csv.DictReader(csvfile, quoting=csv.QUOTE_NONNUMERIC, fieldnames=fieldnames)
                for row in reader:
                    rows.append(row)
        except FileNotFoundError:
            continue # its okay if we are missing data

    # only show most recent chage if no days passed
    if days == None:
        rows = [ rows[-1] ]

    # enrich with the scaled wattage
    wattageScale = getWattageScale()
    dataWithWattage = [ row | { "scaled wattage": row[ChargeKeys.PV_power_L] * wattageScale } for row in rows ]

    # then filter on key
    if key != None:
        return [ { key: row[key], "timestamp": row["timestamp"] } for row in dataWithWattage ]

    return dataWithWattage

# X-Real-Ip is set in the nginx config
@app.get("/api/myip")
def getChargeForDay(x_real_ip: str | None = Header(default=None)):
    return x_real_ip

def getDNSKey():
    filename = f"/data/dnskey.txt"

    with open(filename, "r") as dnskeyfile:
        return readline()

@app.get("/api/allowlist")
def allowlist():
    # TODO: swtich to file
    return {
        "Hells Gate": "$2y$10$5/O1zeTvLmxBNIRpmqve5u6x9RmL8JBi./dzgD3mwfudHEBuABFQ6",
        "Chile": "$2y$10$M3RtM5fYwzUXYQJRx1OGDe9oPSAmnApDPlCWpYCpHXcQixCPVaNge",
        "Caddie": "$2y$10$157Qs27b4.gUAHlF0o/i5ufIF/tclJ8GitcIQbgeA9t76XYF0S0Ve",
        "Low_Carbon_Methods": "$2y$10$2vFdQ05rQyGFIbY6WjncE.nZgimUEfIoCQKoQmK1qNLSPfc3T2NXy",
        "Dominica": "$2y$10$MLdkxh3qzwwU0yucGTBte.964aMIPxRHa4UiH3o0AH67jGk5P5nDu",
        "Kenya": "$2y$10$3EuwWV0KuoBhBBJd3Q7uX.2XHNIYZZkn0mpUjXSLHd6vGFlAXhyGe",
        "Fiber_Fest": "$2y$10$42gKyu4kJeMnbOn79hJyQOBxE3aqV1OCXSwaWasg1Dvi0goII2fKK",
        "Swarthmore ": "$2y$10$43RlEFdYJqqc5Odvnr.ol.pbJ0A.p7td3rIzz4Z3V56KpQ0cLogJe"
    }

@app.get("/api/blocklist")
def blocklist():
    # TODO: switch to file
    # TODO: extend to support multiple burned keys from the same server
    return {
        "Tega": "",
        "SPfA": "$2y$10$8jr3efgV3/N2RosUY0cH1edYXYcYNE4Iwi6RHqYwyupnccYVX9f5.",
        "Beijing": "$2y$10$0uZh7HjT27KTN5uszOCuxe6yhEWbWxzX/i/ZY1vIfZg1xqfNgshmS"
    }

@app.post("/api/ip")
def updateDNS(key: str, ip: str):
    name = verifyPasswordAndReturnName(key)

    params = {
        host: '@',
        domain: 'solarprotocol.net',
        password: key,
        ip: ip
    }

    response = request.get("https://dynamicdns.park-your-domain.com/update", params=params)
    if response.status == 200:
        updatePoeLog(name, ip)

def verifyPasswordAndReturnName(key: str):
    for name, hash in allowList():
        if key == hash:
            return name

    raise Exception('Incorrect password')

def updatePoeLog(name: str, ip: str):
    fileName = f"/data/dns.log"

    with open(fileName, "a", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[name, ip])
        writer.writerow([name, ip])


@app.post("/api/profile")
def updateProfileImage(profile: str):
    fileName = f"/local/serverprofile.gif"

    with open(fileName, "w") as profilefile:
        write(profile, profilefile)

@app.get("/api/local")
def getLocal(key: Union[SystemKeys, None]):
    filename = f"/local/local.json"

    with open(filename, "r") as jsonfile:
        localData = json.load(jsonfile)

    if key == None:
        safe_data = { key: getLocal(key) for key in safe_keys }
        safe_data["timezone"] = getTimezone()
        safe_data["wattage-scale"] = getWattageScale()
        return safe_data
        
    if key == "color":
        return localData["bgColor"]

    return localData[key]

@app.post("/api/local")
def updateProfileImage(
    name: Union[str, None] = Form(),
    description: Union[str, None] = Form(),
    location: Union[str, None] = Form(),
    city: Union[str, None] = Form(),
    country: Union[str, None] = Form(),
    lat: Union[str, None] = Form(),
    lon: Union[str, None] = Form(),
    pvWatts: Union[str, None] = Form(),
    pvVolts: Union[str, None] = Form(),
):
  formData = {
      "name": name,
      "description": description,
      "location": location,
      "city": city,
      "country": country,
      "lat": lat,
      "lon": lon,
      "pvWatts": pvWatts,
      "pvVolts": pvVolts
  }
  
  # filter out empty or none
  filtered = { key: value for (key, value) in formData.items() if value }
  
  filename = f"/local/local.json"
  with open(filename, "r") as localfile:
      local = json.load(localfile)

  local.update(filtered)

  with open(filename, "w") as localfile:
      json.dump(local, localfile)
  
  def frontend_admin_settings():
      return '''<?php
  //read local file
  $localFile = '/home/pi/local/local.json';
  $imgDir = '/home/pi/local/www/';

  $spenv = '/home/pi/local/.spenv';

  $localInfo = json_decode(getFile($localFile), true);

  $apiErr = $dnsErr = $httpErr = "";

  if ($_SERVER["REQUEST_METHOD"] == "POST") {
      if (isset($_POST['key']) && $_POST['key'] == "form") {
          //handle the form data

          for ($k = 0; $k < count(array_keys($_POST));$k++) {
              //echo array_keys($_POST)[$k];

              if (isset($_POST['apiKey'])) {
                  if (empty($_POST['apiKey'])) {
                      $apiErr = "No data entered.";
                  } else {
                      //$localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
                      setEnv('API_KEY', $_POST['apiKey']);
                      //echo('API key received');
                  }
              } elseif (isset($_POST['dnsPW'])) {
                  if (empty($_POST['dnsPW'])) {
                      $dnsErr = "No data entered.";
                  } else {
                      //$localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
                      setEnv('DNS_KEY', $_POST['dnsPW']);
                      //echo('DNS key received');
                  }
              } elseif (isset($_POST['httpPort'])) {
                  if (! is_numeric($_POST['httpPort']) || strpos($_POST['httpPort'], '.')) {
                      $httpErr = "Port value is not an integer.";
                  } else {
                      $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
                  }
              } else {
                  $localInfo[array_keys($_POST)[$k]]= test_input($_POST[array_keys($_POST)[$k]]);
              }
          }

          file_put_contents($localFile, json_encode($localInfo, JSON_PRETTY_PRINT));
      } elseif (isset($_POST['key']) && $_POST['key'] == "file") {
          //handle the file
          //echo "file";
          Upload\uploadIt();
      }
  }

  if (isset($localInfo["httpPort"])) {
      $httpPort = $localInfo["httpPort"];
  } else {
      $httpPort = "80"; //display default port if no custom port info is found
  }

  //front end form for https needed
  /*if (isset($localInfo["httpsPort"])){
    $httpPort = $localInfo["httpsPort"];
  }*/

  function test_input($data)
  {
      /* $data = str_replace("\r", " ", $data) //rm line breaks
       $data = str_replace("\n", " ", $data) //rm line breaks
       $data = str_replace("  ", " ", $data) //replace double spaces with single space*/
      $data = str_replace(array("\n", "\r", "  "), ' ', $data);
      $data = trim($data);
      $data = stripslashes($data);
      $data = htmlspecialchars($data);
      return $data;
  }

  //add in a validation test?
  /*function testAPIkey($data){
    echo !empty($data);
    if(!empty($data)){
      return true;
    } else {
      return false;
    }
  }*/

  function getFile($fileName)
  {
      //echo $fileName;
      try {
          return file_get_contents($fileName);
      } catch(Exception $e) {
          echo $fileName;
          return false;
      }
  }

  function setEnv($envKey, $envVal)
  {
      global $spenv;
      //test inputs
      $envKey = test_input($envKey);
      $envVal = test_input($envVal);

      /*  $execCmd = escapeshellcmd("bash /home/pi/solar-protocol/backend/set_env.sh \"${envKey}\" \"${envVal}\"");

        exec($execCmd, $shOutput);

        var_dump($shOutput);*/
      if (file_exists($spenv)) {
          //read in file
          $envVar = file($spenv);

          //var_dump($envVar);

          $newEnv = fopen($spenv, "w");

          for ($l = 0; $l < count($envVar); $l++) {
              if (strpos($envVar[$l], "export {$envKey}=") === false && $envVar[$l] !== "" && $envVar[$l] !== "\n") {
                  fwrite($newEnv, $envVar[$l]);
              }
          }

          fwrite($newEnv, "export {$envKey}={$envVal}\n");
          fclose($newEnv);
      } else {
          $output = "export {$envKey}={$envVal}\n";
          /*    echo $output;*/
          $newEnv = fopen($spenv, "w");
          fwrite($newEnv, $output);
          fclose($newEnv);
      }
  }
  ?>
  '''