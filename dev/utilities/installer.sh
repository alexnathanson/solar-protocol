#!/bin/bash
set -e
set -u
set -o pipefail

echo 'Solar Protocol Installer v1.0'
echo
prompt 'Have you configured your pi with raspi-config?'

echo 'updating OS'; {
  sudo apt-get update --yes
  sudo apt-get upgrade --yes
}

echo 'getting the latest code'; {
  cd /home/pi
  test -d solar-protocol || git clone http://www.github.com/alexnathanson/solar-protocol
  cd solar-protocol
  git pull --rebase
}

echo "installing podman and podman-compose"; {
  sudo apt-get install podman podman-compose --yes
}

echo "building the latest images"; {
  bash dev/build
}

echo "Adding our ssh keys"; {
  install -d -m 700 ~/.ssh
  sudo mv /home/pi/solar-protocol/utilities/authorized_keys /home/pi/.ssh/authorized_keys
  sudo chmod 644 /home/pi/.ssh/authorized_keys
  sudo chown pi:pi /home/pi/.ssh/authorized_keys
}

echo "starting the service"; {
  bash dev/start
}

prompt() {
  read -p "$* (y/N)" confirm && \
    [[ $confirm == [yY] || $confirm == [yY][eE][sS ]] \
    || exit 1
}
