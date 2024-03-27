#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
set -e
if [[ -f secrets ]]; then source secrets ; else echo "no secrets" ; fi

export VERSION=${1:-local}
export REF_IMAGE_VERSION=${1:-local}
export SYSTEM_NAME=${1:-$(basename $(pwd))}
export SYSTEM_NAME=image_search

echo "**** ${SYSTEM_NAME} docker build"
./docker/${SYSTEM_NAME}/build.sh ${VERSION} ${VERSION}

echo "**** ${SYSTEM_NAME} unit test"
./docker/${SYSTEM_NAME}_unit_test/build.sh ${VERSION} ${VERSION}
./docker/${SYSTEM_NAME}_unit_test/test_in_docker.sh
