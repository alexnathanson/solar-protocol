# developing solar protocol

We use containers to make it easier to manage our code dependencies.

## services

There are 4 services that make up the entire protocol:

### 1. solar-protocol service

The solar protocol is supervised by `[protocol/run.py](/protocol/run.py)`. This runner runs a number of other scripts, depending on the current solar and battery conditions:

1. clientPostIP

Updates all devices found in devices.json with its own device information - `api_key`, `timestamp`, `ip`, `mac`, `name`, `timezone`, and `poelog`.

2. solarProtocol

Queries all devices in the devicelist for their scaled-wattage, and if the current device should be the point of entry, update the dns records

3. getRemoteData

This collects the photovoltaic data from remote servers via the open data API.

4. viz

Updates the clock visualizations. This only runs if the device has 30% or more battery power.

5. create_html

Regenerates the website with the latest data

### 2. charge controller service

The charge controller service periodically reads the charge controller and saves a log for the other scripts

### 3. api service

This api allows other devices in the network to query the server for public info

### 4. web service

This is an nginx proxy that serves up the static files made by the solar-protocol service, as well as delegating to the api service


## getting started - install instructions

All commands are kept in the `solar-protocol` so everyone can stay up-to-date with installing, debugging, and developing the protocol.

### Clone this code in your home directory

    sudo apt-get install --yes git
    git clone https://github.com/alexnathanson/solar-protocol.git
    cd solar-protocol

### Install dependencies

    ./solar-protocol init

Once dependencies are installed, you can use the 'solar-protocol' command without the `./` prefix

    solar-protocol help

Run the server - this will bring it up in development mode, which will have live code reloading, and not post information to the live network.

    solar-protocol dev

Next, generate the initial static site

    solar-protocol generate

Visit the blank site on http://127.0.0.1:11221

    solar-protocol open

Congrats! You should see the pizza rat server!
