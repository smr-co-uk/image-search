#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export VERSION=${1:-local}
BASE_VERSION=${2:-local}
IMAGE_NAME=$(basename $(pwd))
if [[ -f ../env.sh ]]; then source ../env.sh ; else echo "no env, exiting"; exit 1 ; fi

IMAGE=${REGISTRY}/${IMAGE_NAME}

cd ../..

echo "Building ${IMAGE}:${VERSION}"
docker build --ssh default ${PLATFORMS}  \
    -f docker/${IMAGE_NAME}/Dockerfile \
    --build-arg BASE_VERSION=${BASE_VERSION} \
    -t ${IMAGE}:${VERSION} \
     .
