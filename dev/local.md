# Developing without containers

# Install php, apache, and configure them

Read [docs/installation.md](../docs/installation) to install and setup php and apache2 manually.

> Note: this is done for you if you use containers + the scripts in this folder

## Creating and activating the python virtual environment

These instructions come from [this pip and virtual env guide][], which provides syntax for both Unix/MacOS and Windows.

[this pip and virtual env guide]: https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment

You should create a virtual environment called 'env'. This will create a folder called env. (This is in the .gitignore and wont get pushed to the repo.)

### Create the virtual environment

Navigate to the solar-protocol root directory. Build a virtual environment.

    python3 -m venv env # note the python3 may change depending on your OS and environment paths

### Activate the python virtual environment

Unix/MacOS

    source env/bin/activate

Windows

    .\env\Scripts\activate

### Leaving the environment

Use command `deactivate` to exit the virtual environment. (This is the same regardless of OS.)

### Installing packages

Install the dependencies from our requirements file, which is located in the solar-protocol root directory

    python3 -m pip install --requirement requirements.txt

