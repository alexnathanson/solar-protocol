# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/

from time import sleep
import datetime
import numpy as np
import pandas as pd
import csv
import os
import sys
import platform

#the syntax for the unit arguments changes depending on which version of pymodbus is running
unit = 1

#check which version of Python is running.
#Python version >= 3.8 require pymodbus version 3.2.2 which has slightly different syntax
if int(platform.python_version()[0] + platform.python_version()[2]) >= 38:
    try:
        from pymodbus.client import ModbusSerialClient as ModbusClient
    except Exception as e:
        print(e)
        print(f"You are running a Python version >= 3.8 so you must be using pymodbus 3.2.2 or greater.")
        print(f"Check your pymodbus version with this code: pip show pymodbus")
        print(f"or try upgrading with this code: pip install --upgrade pymodbus")
else:
    try:
        from pymodbus.client.sync import ModbusSerialClient as ModbusClient
        #change the syntax for unit
        unit = 'unit=' + str(unit)
    except Exception as e:
        print(e)
        print(f"You are running a Python version < 3.8 so you must be using pymodbus 2.5.3.")
        print(f"Check your pymodbus version with this code: pip show pymodbus")
        print(f"or try installing the specific version of pymodbus with this code: pip install -U pymodbus==2.5.3")

client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 115200)

try:
    client.connect()

    while True:
        result = client.read_input_registers(0x3100,16,unit)
        result2 = client.read_input_registers(0x311A,2,unit)

        if not result.isError() and not result2.isError():
            pvVoltage = float(result.registers[0] / 100.0)
            pvCurrent = float(result.registers[1] / 100.0)
            pvPowerL = float(result.registers[2] / 100.0)
            pvPowerH = float(result.registers[3] / 100.0)
            batteryVoltage = float(result.registers[4] / 100.0)
            batteryCurrent = float(result.registers[5] / 100.0)
            batteryPowerL = float(result.registers[6] / 100.0)
            batteryPowerH = float(result.registers[7] / 100.0)
            loadVoltage = float(result.registers[8] / 100.0)
            loadCurrent= float(result.registers[9] / 100.0)
            loadPower= float(result.registers[10] / 100.0)

            batteryPercentage = float(result2.registers[0] / 100.0)

            newDF = pd.DataFrame(data={
                "datetime" : [datetime.datetime.now()],
                "PV voltage": [pvVoltage],
                "PV current": [pvCurrent],
                "PV power L": [pvPowerL],
                "PV power H": [pvPowerH],
                "battery voltage":[batteryVoltage],
                "battery current":[batteryCurrent],
                "battery power L":[batteryPowerL],
                "battery power H": [batteryPowerH],
                "load voltage":[loadVoltage],
                "load current": [loadCurrent],
                "load power": [loadPower],
                "battery percentage": [batteryPercentage]})

            # create a new file daily to save data
            # or append if the file already exists
            fileName = '/home/pi/solar-protocol/charge-controller/data/tracerData'+str(datetime.date.today())+'.csv'
            try:
                with open(fileName) as csvfile:
                    df = pd.read_csv(fileName)
                    #append needs to be changed to concat
                    #something like: df = pd.concat([df,newDF], ignore_index = True)
                    df = df.append(newDF, ignore_index = True)
                    df.to_csv(fileName, sep=',',index=False)
            except:
                newDF.to_csv(fileName, sep=',',index=False)

            #print(newDF)
            print("csv writing: " + str(datetime.datetime.now()))

        else:
            print("error: {}".format(result))

        # runs every x-second
        sleep(60*2)

except Exception as e:
    print(e)
    print(f"Could not connect to charge controller! Confirm pymodbus version matches Python version or check physical connection to charge controller")
    sys.exit(1)

client.close()
