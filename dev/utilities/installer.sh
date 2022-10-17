#!/bin/bash
set -e
set -u
set -o pipefail

prompt() {
  read -p "$* (y/N)" confirm && \
    [[ $confirm == [yY] || $confirm == [yY][eE][sS ]] \
    || exit 1
}

echo 'Solar Protocol Installer V0.0.1 - UNTESTED!!!'
echo
prompt 'Have you configured your pi with raspi-config?'

###### OS ######

echo 'updating OS'
sudo apt update

echo 'upgrading OS'
sudo apt upgrade

###### CODE ######
echo 'cloning repository'

#clone the git repository
cd /home/pi
test -d solar-protocol || git clone http://www.github.com/alexnathanson/solar-protocol

#copy the local directory to outside the repository
sudo cp -r /home/pi/solar-protocol/local /home/pi/local

###### PYTHON PACKAGES ######
echo 'installing python packages'

sudo apt install python3-pip

pip3 install --requirement requirements.txt 

###### SECURITY ######

###### SERVER ######

echo 'installing web server'

sudo apt install apache2 php php-gd --yes

#Change Apache default directory to the frontend directory
cd /etc/apache2/sites-available

echo 'Apache configuration is not automated at this time'
echo 'Read configuration instructions with:'
echo 'cat docs/installation.md'

prompt 'Have you configured the apache server?'

###### AUTOMATION ######

echo 'automating charge controller data collection'

echo 'automate charger controller runner'
