if ! command -v docker 2>/dev/null; then
  echo >&2 "missing docker, exiting"
  exit 1
fi

current_directory=$PWD
cd "$(dirname -- "$0")"

echo "updating pi-gen"; {
  test -d pi-gen || git clone https://github.com/RPi-Distro/pi-gen
  if [[ "$(uname -m)" == "arm64" ]]
  then
    git -C pi-gen switch arm64
  fi
  git -C pi-gen pull
}

if [[ "$CI" == "true" ]]; then
  apt install -y < pi-gen/depends
else
  rm -rf pi-gen/stage-solar pi-gen/config
  docker rm -v pigen_work
fi

echo "updating config"; {
  export PUBKEY_SSH_FIRST_USER="$(<../authorized_keys)"
  export FIRST_USER_PASS=$(openssl rand -hex 16)
  GIT_REV=${GITHUB_SHA:-HEAD}
  export VERSION=1.1-$(git rev-parse --short $GIT_REV)
  cp -r stage-solar pi-gen/
  rm -rf pi-gen/stage2/EXPORT_IMAGE
  envsubst < config.template > pi-gen/config
}

echo "building"; {
  bash pi-gen/build-docker.sh
  cp pi-gen/deploy/*.xz ${starting_directory}/
  ls ${starting_directory}/*xz
}
