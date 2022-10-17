# developing solar protocol

We use containers to make it easier to manage our code dependencies.

## services

There are 4 services that make up the entire protocol:

### 1. solar-protocol service

The solar protocol is supervised by `[protocol/run.py](/protocol/run.py)`. This runner runs a number of other scripts, depending on the current solar and battery conditions:

1. clientPostIP

Updates all devices found in devicelist.json with its own device information - `api_key`, `timestamp`, `ip`, `mac`, `name`, `timezone`, and `poelog`.

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

Always check [the latest podman installation docs](https://podman.io/getting-started/installation), but as a nicety, try this:

### linux

    sudo apt install podman podman-compose

### macOS

    brew install podman podman-compose
    podman machine init --volume /Users

> Ignore any `Error: exit status 255` messages

Why the `--volume /Users`?

Podman (and Docker) require linux to do containerization, so if we want to run them on macOS, we have to start a linux virtual machine. And we first need to mount files from macOS to linux, before we can use them in our containers. This can be done from the commandline or using the Podman Desktop or Docker Desktop guis. Either way, this is what will be happening in the background:

    macOS (host)
     -> podman machine (linux)
         -> solar-protocol-dev (container)

### Windows

See [the official windows install docs](https://github.com/containers/podman/blob/main/docs/tutorials/podman-for-windows.md)

## build the base image

First, make sure you have the correct ssh keys and podman machine is running

> Note: On macOS you may want to `ssh-add ~/.ssh/podman-machine-default`

    podman machine start

Now, build a known good version of python and our dependencies

    bash dev/build

## Run the server

This will bring up the server

    bash dev/start

Next, regenerate the site

    bash dev/generate

Visit the blank site on http://127.0.0.1:11221

    open http://127.0.0.1:11221

Now, lets generate a fresh version of the website

    bash dev/generate

Congrats! You should see the pizza rat server!

## development scripts

We have a few scripts to make it easier to develop. All are based on containers, using podman to maintain images.

* `dev/build` - makes a container image, with all the dependencies and code to run the solar protocol in a virtual machine

* `dev/start` - starts a virtual machine using the container image
