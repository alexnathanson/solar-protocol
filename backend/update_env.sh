#!/bin/sh

$key = $1
$val = $2

$ nano /etc/environment

export $key=$val

#export NETWORK_KEY='test'