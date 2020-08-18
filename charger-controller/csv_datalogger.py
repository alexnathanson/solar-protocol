# pymodbus code based on the example from http://www.solarpoweredhome.co.uk/
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from time import sleep
import datetime
import numpy as np
import pandas as pd
import csv
import os


client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 115200)
client.connect()

while True:
    result = client.read_input_registers(0x3100,16,unit=1)
    if not result.isError():
        solarVoltage = float(result.registers[0] / 100.0)
        solarCurrent = float(result.registers[1] / 100.0)
        solarPowerL = float(result.registers[2] / 100.0)
        solarPowerH = float(result.registers[3] / 100.0)
        batteryVoltage = float(result.registers[4] / 100.0)
        batteryCurrent = float(result.registers[5] / 100.0)
        batteryPowerL = float(result.registers[6] / 100.0)
        batteryPowerH = float(result.registers[7] / 100.0)
        loadVoltage = float(result.registers[8] / 100.0)
        loadCurrent= float(result.registers[9] / 100.0)
        loadPower= float(result.registers[10] / 100.0)

        result = client.read_input_registers(0x311A,2,unit=1)
        if not result.isError():
            batteryPercentage = float(result.registers[0] / 100.0)

            newDF = pd.DataFrame(data={
                "datetime" : [datetime.datetime.now()],
                "solarVoltage": [solarVoltage],
                "solarCurrent": [solarCurrent],
                "solarPowerL": [solarPowerL],
                "solarPowerH": [solarPowerH],
                "batteryVoltage":[batteryVoltage],
                "batteryCurrent":[batteryCurrent],
                "batteryPowerL":[batteryPowerL],
                "batteryPowerH": [batteryPowerH],
                "loadVoltage":[loadVoltage],
                "loadCurrent": [loadCurrent],
                "loadPower": [loadPower],
                "batteryPercentage": [batteryPercentage]})

            # create a new file daily to save data
            # or append if the file already exists
            fileName = 'data/tracerData'+str(datetime.date.today())+'.csv'
            try:
                with open(fileName) as csvfile:
                    df = pd.read_csv(fileName)
                    df = df.append(newDF, ignore_index = True)
                    df.to_csv(fileName, sep=',',index=False)
            except:
                newDF.to_csv(fileName, sep=',',index=False)

            #print(newDF)
            print("csv writing: " + str(datetime.datetime.now()))

    else:
        print("error: {}".format(result))

    # runs every x-second
    sleep(60*5)

client.close()
