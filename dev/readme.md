# development scripts

these scripts are based on containers - you will want podman installed.

If you prefer to develop without containers, check out [local.md](./local.md)

## start

starts a container with the latest version

use `podman ps` to determine what port apache2 started on

## build

makes a container image 

## watch

rebuilds the image when Containerfile changes

# development setup

We use containers because python package management is painful. These docs are for podman and podman-compose, but it should work the same with docker and docker compose.

## install required tools

Always check [the latest podman installation docs](https://podman.io/getting-started/installation)

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

    ssh-agent add ~/.ssh/podman-machine-default
    podman machine start

Now, build a known good version of python and our dependencies

    bash dev/build

## Run the server

This will bring up the server

    bash dev/start

Next, regenerate the site

    bash dev/generate

Visit the blank site on http://127.0.0.1:43753

    open http://127.0.0.1:43753

Now, lets generate a fresh version

    bash dev/generate
