# Tracer Charge Controller Data Logger

These scripts enable logging data from an Epever Tracer-AN Series charge controller connected to a Raspberry Pi via a USB to RS485 converter (ch340T chip model). Currently, we use CVS_datalogger.py

* This is run at start up via rc.local (see <a href="https://github.com/alexnathanson/solar-protocol/blob/master/installation.md">installation.md</a> for complete instructions)

## Wiring

* RJ45 blue => b
* RJ45 green => a

## Installation
Install pymodbus
`sudo pip3 install pymodbus`


