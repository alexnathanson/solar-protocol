# Developing

Instructions for developing the Solar Protocol

Helpful scripts for developing are in the dev/ folder.

## Code introduction

Some of the solar protocol scripts rely on the open API and some require private API access.

There are three backend scripts that rebuild the static site based on the latest data, which do not POST data anywhere 

1. core/getRemoteData
2. createHTML/viz
3. createHTML/create_html

There are two protocol scripts that require API keys, and will fail in dev.
More work is needed to enable them to safely make test posts with dummy data without it breaking the client.

1. clientPostIP.py
2. solarProtocol.py

All of these scripts should be run with the DEV arg, e.g. `python3 solar-protocol/backend/createHTML/create_html.py DEV`

Static example data for these scripts lives in the dev/data/ folder. Data/files created from these scripts is saved to the dev/data/temp folder and is ignored from the repo.

## Development environment

There are two ways to develop the software - one uses containers, which is more convinient and robust.

For normal development, please read [dev/readme.md](../dev/readme.md). This is recommended when developing on a personal computer, and most of the useful scripts in `dev/` require it.

For 'local' development, please read [dev/local.md](../dev/local.md). If you prefer running the software directly on your operating system, this will require less resources, but more manual setup.

# Troubleshooting

When sharing issues, please provide testing data in the dev/data/ directory

## Logs

Backend core logs are located in the /home/pi/solar-protocol/backend/runner.log

Apache and PHP errors are logged in /var/log/apache2/error.log

## Is it running?

    ps aux | grep .py
