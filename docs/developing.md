# Installation

First we install python, some native dependencies, and python dependencies.

    ./scripts/install-macos-dependencies
    ./scripts/install-python-dependencies



## Quick Start (macOS)

    git clone --branch beta https://github.com/alexnathanson/solar-protocol
    cd solar-protocol

    ./scripts/install-macos-dependencies
    ./scripts/install-python-dependencies
    ./run

# Development

## Services

There are 4 services that make up the entire protocol. 

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
