# developing solar protocol

We use containers to make it easier to manage our code dependencies.

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

We ran into issues installing podman **4.3.0-RC1**, so make sure you are using the latest full release.

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

Visit the blank site on http://127.0.0.1:43753

    open http://127.0.0.1:43753

Now, lets generate a fresh version of the website

    bash dev/generate

Congrats! You should see the pizza rat server!

## development scripts

We have a few scripts to make it easier to develop. All are based on containers, using podman to maintain images. If you prefer to develop without containers, check out [local.md](./local.md).

* `dev/build` - makes a container image, with all the dependencies and code to run the solar protocol in a virtual machine

* `dev/start` - starts a virtual machine using the container image

* `tests/viz` - grabs the active visualization and deviceList, generates the viz locally, and shows the difference
