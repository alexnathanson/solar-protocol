# Installation

First we install podman - which will run our containers, then we install podman-desktop, a gui to make it easier to explore those containers.

Solar Protocol targets [debian linux](https://debian.org) because thats what runs on a Raspberry Pi. One reason we use podman is to allow development on macOS and windows.

## Quick Start (linux)

    git clone --branch beta https://github.com/alexnathanson/solar-protocol && cd solar-protocol

    ./solar install  # asks to install podman, podman-compose, and necessary dependencies
    solar start      # starts the server
    solar open       # opens the local server

1. Setup podman and podman-compose

Always check [the latest podman installation docs](https://podman.io/getting-started/installation).

For windows, follow [the official windows install docs](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md).

For linux, install podman with your package manager:

    sudo apt-get install --yes podman

For macOS, install podman with [homebrew](https://brew.sh):

    brew install podman

For windows, linux, and macOS, install podman-compose using pip:

    pip3 install podman-compose

2. Setup solar-protocol

All commands are kept in the `solar` commandline script so everyone can stay up-to-date with installing, debugging, and developing the protocol.

Install git. For example, on linux:

    sudo apt-get install --yes git

Clone the latest `beta` branch

    git clone --branch beta https://github.com/alexnathanson/solar-protocol.git
    cd solar-protocol

Add the solar script to your commandline PATH

    ./solar install

Build the base images

    solar build

This will bring up the server

    solar start

Visit the blank site on http://127.0.0.1:11221

    solar open

Congrats! You should see the pizza rat server!

## Troubleshooting

To view backend protocol logs

    solar logs protocol

To view web server logs

    solar logs web

To view api logs

    solar logs api

Sharing these logs will make it easier for people to help

### Running discrete scripts

It can be helpful to run scripts manually

    solar exec protocol python core/solarProtocol.py

To run manually with full logs

    solar exec --env LOGLEVEL=debug protocol python core/solarProtocol.py

If running a script manually will introduce a race condition you will need to stop the script. This is especially likely with the datalogger script, because its sole purpose is to write data to a file.

    solar stop datalogger
    solar exec datalogger python csv_datalogger.py
    solar start datalogger

# Development

## Services

There are 4 services that make up the entire protocol. `solar status` should show something like this:

    CONTAINER ID  IMAGE                                       COMMAND               CREATED        STATUS                             PORTS                  NAMES
    239ae01f12a5  localhost/solar-protocol/datalogger:beta  /bin/sh -c python...  5 minutes ago  Exited (1) Less than a second ago                         solar-protocol_datalogger_1
    d94bd414c5f8  localhost/solar-protocol/api:beta         uvicorn api:app -...  5 minutes ago  Up 4 minutes ago                   0.0.0.0:11215->80/tcp  solar-protocol_api_1
    438b0c5c552d  localhost/solar-protocol/protocol:beta    python run.py now     4 minutes ago  Up 4 minutes ago                                          solar-protocol_protocol_1
    887fc54be131  docker.io/library/nginx:beta              nginx -g daemon o...  4 minutes ago  Up 4 minutes ago                   0.0.0.0:11221->80/tcp  solar-protocol_web_1

### 1. protocol service

The solar protocol is supervised by [protocol/run.py][]. This runner runs a number of other scripts, depending on the current solar and battery conditions.

This includes two scripts that manage the peer-to-peer network - [protocol/core/publishDevice.py][], and [protocol/solarProtocol.py].

 are three scripts that rebuild the static site based on the latest data - `core/getRemoteData.py`, `build/viz.py`, and `build/html.py`.

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

The datalogger service periodically reads the charge controller and saves a log for the other scripts. If it is not running on a raspberry pi, it fakes data. You can also force faking data by exporting `FAKE_DATA=True`. If you are using systemd (as the Raspberry Pis are), you should edit `/etc/systemd/system/solar-protocol.service.d/datalogger.conf`.

### 3. api service

This api allows other devices in the network to query the server for public info.

### 4. web service

This is an nginx proxy that serves up the static files made by the solar-protocol service, as well as delegating to the api service.


## Contributing

Please install `ruff` via `cargo install ruff` and run `solar format` before making pull requests.
