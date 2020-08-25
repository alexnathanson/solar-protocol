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
    #doesn't need to happen every time, just at midnight
    #fileName = '/home/pi/Desktop/EPSolar_Tracer/data/tracerData'+str(datetime.date.today())+'.csv' 

    result = client.read_input_registers(0x3100,16,unit=1)

    solarVoltage = float(result.registers[0] / 100.0)
    solarCurrent = float(result.registers[1] / 100.0)
    solarPowerL = float(result.registers[2] / 100.0)
    solarPowerH = float(result.registers[3] / 100.0)
    
    print("solarVoltage: " + str(solarVoltage))
    print("solarCurrent: " + str(solarCurrent))
    print("solarPowerL: " + str(solarPowerL))
    print("solarPowerH: " + str(solarPowerH))
    print()
    
    batteryVoltage = float(result.registers[4] / 100.0)
    battetyChargingCurrent = float(result.registers[5] / 100.0)
    battetyChargingPowerL = float(result.registers[6] / 100.0)
    battetyChargingPowerH = float(result.registers[7] / 100.0)
    
    print("batteryVoltage: " + str(batteryVoltage))
    print("battetyChargingCurrent: " + str(battetyChargingCurrent))
    print("battetyChargingPowerL: " + str(battetyChargingPowerL))
    print("battetyChargingPowerH: " + str(battetyChargingPowerH))
    print()

    loadVoltage = float(result.registers[8] / 100.0)
    loadCurrent = float(result.registers[9] / 100.0)
    loadPowerL = float(result.registers[10] / 100.0)
    loadPowerH = float(result.registers[11] / 100.0)
    
    print("loadVoltage: " + str(loadVoltage))
    print("loadCurrent: " + str(loadCurrent))
    print("loadPowerL: " + str(loadPowerL))
    print("loadPowerH: " + str(loadPowerH))
    print()

    sleep(5)

client.close()