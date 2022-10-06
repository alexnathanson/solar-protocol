# development scripts

these are based on containers - you will want podman or docker installed

# generate

run the three backend scripts that rebuild the static site based on the latest data

  1. core/getRemoteData
  2. createHTML/viz
  3. createHTML/create_html

# start

starts a container with the latest version

use `podman ps` to determine what port apache2 started on

# build

makes a container image 

# watch

rebuilds the image when Containerfile changes
