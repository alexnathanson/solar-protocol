#!/bin/bash

#NOT TESTED YET!!!
# prior to this, configure the device with raspi-config
# after this, complete the security installation steps manually

echo 'Solar Protocol Installer V0.0.1 - NOT TESTED YET!!!'

###### OS ######
#update and upgrade your pi

echo 'updating OS'
sudo apt update

echo 'upgrading OS'
sudo apt upgrade

###### REPOSITORY ######
echo 'cloning repository'

#clone the git hub repository
cd /home/pi
test -d solar-protocol || git clone http://www.github.com/alexnathanson/solar-protocol

#copy the local directory to outside the repository
sudo cp -r /home/pi/solar-protocol/local /home/pi/local

#set permissions for all SP files
sh /home/pi/solar-protocol/utilities/setAllPermissions.sh

###### PYTHON PACKAGES ######
echo 'installing python packages'

sudo apt-get install python3-pip

pip3 install -r requirements.txt 

###### SECURITY ######

###### SERVER ######

echo 'installing Apache server'
echo 'Apache configuration is not automated at this time.'
echo 'See configuration instructions at:'
echo 'https://github.com/alexnathanson/solar-protocol/blob/master/installation.md'

# install Apache
sudo apt-get install apache2 -y

# install PHP
sudo apt-get install php -y

#Change Apache default directory to the frontend directory
cd /etc/apache2/sites-available


###### AUTOMATION ######

echo 'automating charge controller data collection'

echo 'automate charger controller runner'