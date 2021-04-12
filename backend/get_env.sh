#!/bin/bash

#argumment 1 is the name of the environmental variable
source /home/pi/local/.spenv

printf '%s\n' "${!1}"