# Local Directory

This directory contains settings that are unique to each server

## local.json

### httpPort [number]

if you need to change the port you are serving from

### interface [wlan0 | eth0]

How the server connects to the internet. Defaults to `wlan0` but change to `eth0` if you are wired in.

## secrets.json

### apiKey

What key other servers should use to access your server's api

### dnsPassword

Needed for updating dns entries
