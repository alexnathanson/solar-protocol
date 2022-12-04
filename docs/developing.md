# Developing

Instructions for developing the Solar Protocol

Helpful scripts for developing are in the dev/ folder.

If this is the first time you are using containers, we recommend installing [Podman Desktop](https://podman-desktop.io) to see whats going on.

## Quick Start

    ./solar-protocol install # asks to install podman, podman-compose, and necessary dependencies
    solar-protocol build     # builds the containers
    solar-protocol dev       # starts the server
    solar-protocol generate  # generates static site
    solar-protocol open      # opens the local server

## Services

There are 4 services that make up the entire protocol. `solar-protocol status` should show something like this:

    CONTAINER ID  IMAGE                                       COMMAND               CREATED        STATUS                             PORTS                  NAMES
    239ae01f12a5  localhost/solar-protocol/datalogger:beta  /bin/sh -c python...  5 minutes ago  Exited (1) Less than a second ago                         solar-protocol_datalogger_1
    d94bd414c5f8  localhost/solar-protocol/api:beta         uvicorn api:app -...  5 minutes ago  Up 4 minutes ago                   0.0.0.0:11215->80/tcp  solar-protocol_api_1
    438b0c5c552d  localhost/solar-protocol/protocol:beta    python run.py now     4 minutes ago  Up 4 minutes ago                                          solar-protocol_protocol_1
    887fc54be131  docker.io/library/nginx:beta              nginx -g daemon o...  4 minutes ago  Up 4 minutes ago                   0.0.0.0:11221->80/tcp  solar-protocol_web_1

### 1. protocol service

The solar protocol is supervised by `[protocol/run.py](/protocol/run.py)`. This runner runs a number of other scripts, depending on the current solar and battery conditions.

This includes two protocol scripts that manage the peer-to-peer network - `publishDevice.py`, and `solarProtocol.py`.

> Note: More work is needed to enable the protocol scripts to safely make test posts with dummy data without it breaking the client.

There are three scripts that rebuild the static site based on the latest data - `core/getRemoteData.py`, `build/viz.py`, and `build/html.py`.

All of these scripts with should be run with the DEV arg, e.g. `python3 solar-protocol/protocol/build/html.py DEV`. Otherwise they will post data in the real network.

1. publishDevice

Updates all devices found in devices.json with its own device information - `api_key`, `timestamp`, `ip`, `mac`, `name`, `timezone`, and `poelog`.

2. solarProtocol

Queries all devices in the device list for their scaled-wattage, and if the current device should be the point of entry, updates the dns records.

3. getRemoteData

This collects the photovoltaic data from remote servers via the open data API, which is needed for building the html and determining the point-of-entry server.

4. build/viz

Updates the clock visualizations. This only runs if the device has 30% or more battery power.

5. build/html

Regenerates the website with the latest data.

### 2. datalogger service

The datalogger service periodically reads the charge controller and saves a log for the other scripts. In DEV mode, makes up fake data.

### 3. api service

This api allows other devices in the network to query the server for public info.

### 4. web service

This is an nginx proxy that serves up the static files made by the solar-protocol service, as well as delegating to the api service.

## Development Environment Setup


### Setup podman and podman-compose

Always check [the latest podman installation docs](https://podman.io/getting-started/installation).

We require podman-compose 1.0.4, which may not be packaged for your os. In that case, install the development version:

    pip3 install https://github.com/containers/podman-compose/archive/devel.tar.gz

#### Windows

See [the official windows install docs](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md)

### Installing solar-protocol

All commands are kept in the `solar-protocol` so everyone can stay up-to-date with installing, debugging, and developing the protocol.

### Clone this code in your home directory

Install git. For example, on linux:

    sudo apt-get install --yes git

    git clone --branch api-migration-huge-refactor https://github.com/jedahan/solar-protocol.git
    cd solar-protocol

Add solar-protocol script to your commandline PATH

    ./solar-protocol install

Build the base images

    solar-protocol build

This will bring up the server

    solar-protocol dev

Visit the blank site on http://127.0.0.1:11221

    solar-protocol open

Congrats! You should see the pizza rat server!

## Troubleshooting

To view backend protocol logs

   solar-protocol logs protocol

To view web server logs

   solar-protocol logs web

To view api logs

   solar-protocol logs api

Sharing these logs will make it easier for people to help
