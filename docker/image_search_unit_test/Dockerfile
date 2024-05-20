ARG BASE_VERSION=1.0

FROM ghcr.io/smr.co.uk/image_search:${BASE_VERSION} as test_base

USER root

COPY --chown=${APP_USER}:${APP_USER} test_env.yml /tmp/test_env.yml
RUN micromamba install -y -n base --file /tmp/test_environment.yml && \
    micromamba clean --all --yes

FROM test_base

RUN mkdir -p ${APP_HOME}/tests
COPY --chown=${APP_USER}:${APP_USER} tests/photos ${APP_HOME}/tests/photos
COPY --chown=${APP_USER}:${APP_USER} tests/unit/*.py ${APP_HOME}/tests/unit/
#COPY --chown=${APP_USER}:${APP_USER} tests/integration/*.py ${APP_HOME}/tests/integration/
#COPY --chown=${APP_USER}:${APP_USER} tests/integration/docker ${APP_HOME}/tests/integration/docker

WORKDIR ${APP_HOME}

USER ${APP_USER}
CMD pytest tests/unit
