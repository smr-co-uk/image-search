#!/usr/bin/env bash

docker run --rm -v $(pwd)/tests/photos:/opt/root \
    -v $(pwd)/tests/photos:/opt/image \
    ghcr.io/smr.co.uk/image_search:local python -m image_search \
      --verbose \
      --root_dir /opt/root \
      --image /opt/image/positive/1985-06-vitesse_3_negative-positive.jpg
