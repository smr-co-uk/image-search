#!/usr/bin/env bash

docker run --rm -p 8050:8050 -v $(pwd):/opt/images ghcr.io/smr.co.uk/image_search_app:local
#   python3 image_search/dash_app.py --root_dir /opt/images --host 0.0.0.0
