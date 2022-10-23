# Developing

Instructions for developing the Solar Protocol

Helpful scripts for developing are in the dev/ folder.

## Quick Start

    bash dev/init  # asks to install podman, podman-compose, and necessary dependencies
    bash dev/build # builds the container images
    bash dev/start # starts the server
    open http://127.0.0.1:11221

## Services

There are 4 services that make up the entire protocol. `podman-compose --file dev/compose.yaml ps` should show something like this:

### 1. protocol service

The solar protocol is supervised by `[protocol/run.py](/protocol/run.py)`. This runner runs a number of other scripts, depending on the current solar and battery conditions.

This includes two protocol scripts that manage the peer-to-peer network - `clientPostIP.py`, and `solarProtocol.py`.

> Note: More work is needed to enable the protocol scripts to safely make test posts with dummy data without it breaking the client.

There are three scripts that rebuild the static site based on the latest data - `core/getRemoteData.py`, `build/viz.py`, and `build/html.py`.

All of these scripts with should be run with the DEV arg, e.g. `python3 solar-protocol/protocol/build/html.py DEV`. Otherwise they will post data in the real network.

1. clientPostIP

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

Always check [the latest podman installation docs](https://podman.io/getting-started/installation), but as a nicety, try this:

#### linux

    sudo apt install podman podman-compose

#### Windows

See [the official windows install docs](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md)

#### macOS

    brew install podman podman-compose
    podman machine init --volume /Users

> Ignore any `Error: exit status 255` messages

Why the `--volume /Users`?

Podman (and Docker) require linux to do containerization, so if we want to run them on macOS, we have to start a linux virtual machine. And we first need to mount files from macOS to linux, before we can use them in our containers. This can be done from the commandline or using the Podman Desktop or Docker Desktop guis. Either way, this is what will be happening in the background:

    macOS (host)
     -> podman machine (linux host)
         -> solar-protocol-dev (container)

### Run the services

Build the base images

    bash dev/build

This will bring up the server

    bash dev/start

Next, regenerate the viz and website site

    bash dev/generate

Visit the blank site on http://127.0.0.1:11221

    open http://127.0.0.1:11221

Now, lets generate a fresh version of the website

    bash dev/generate

Congrats! You should see the pizza rat server!

## Troubleshooting

Backend core logs are located in the /solar-protocol/protocol/runner.log

Nginx logs are located in /var/log/nginx/error.log

Sharing these logs will make it easier for people to help
