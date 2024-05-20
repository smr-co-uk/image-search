#!/usr/bin/env bash
cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd ..
ENV_NAME=${1:-$(basename $(pwd))}

micromamba env list | grep "${ENV_NAME}"
stat=$?
if [ $stat -ne 0 ] ; then
  echo "Creating env ${ENV_NAME}"
  micromamba create -y --name ${ENV_NAME} --file environment.yml && \
  micromamba install -y --name ${ENV_NAME} --file test_environment.yml
else
  echo "Updating env ${ENV_NAME}"
  micromamba install -y --name ${ENV_NAME} --file environment.yml && \
  micromamba install -y --name ${ENV_NAME} --file test_environment.yml
fi
