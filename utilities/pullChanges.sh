#!/bin/bash

# this is still a work in progress... 

# this does NOT automate anything relating to the local.json config file or ssh keys - those changes must be made manually

# this will also not work if anything needs to be stashed before pulling...

# pull new changes
cd /home/pi/solar-protocol
git stash
git pull origin master

# redo permissions
sh utilities/setAllPermissions.sh
