# Development environment

Instructions for setting up a local development environment for Solar Protocol

Some of the SP scripts rely on the open API and some require private API access. 

Scripts that do not require API keys:
* create_html.py
* viz.py
* getRemoteData.py

## Creating and activating the virtual environment

These instructions come from this link, which provides syntax for both Unix/MacOS and Windows.
https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment

You should create a virtual environment called 'env'. This will create a directory called env. (This is in the git ignore and wont get pushed to the repo.)

### Create the virtual environment

* Navigate to the solar-protocol root directory
*  run `python3 -m venv env` note the python3 may change depending on your OS and environment paths

### Activate it

Unix/MacOS
* `source env/bin/activate`

Windows
* `.\env\Scripts\activate`

### Leaving the environment

Use command `deactivate` to exit the virtual environment. (This is the same regardless of OS.)

### Installing packages

Install the dependencies from our requirements file, which is located in the solar-protocol root directory

`python3 -m pip install -r requirements.txt`

## Running Scripts

To run in unix/MacOS:
`ENV=DEV python3 create_html.py`

To run in Windows:
`python3 create_html.py DEV`

Note that 'python3' may be 'py', 'python', etc. depending on your OS and environment.