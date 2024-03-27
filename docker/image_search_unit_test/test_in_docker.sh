#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [[ -f ../env.sh ]]; then source ../env.sh ; else echo "no env, exiting"; exit 1 ; fi
export VERSION=${1:-local}
IMAGE_NAME=$(basename $(pwd))

cd ../..

mkdir -p $(pwd)/test_results
chmod 777 $(pwd)/test_results
docker run --rm -v $(pwd)/test_results:/opt/app/build ${REGISTRY}/${IMAGE_NAME}:${VERSION}
