ARG MAMBA_BASE_VERSION=1.5-bookworm-slim

FROM mambaorg/micromamba:${MAMBA_BASE_VERSION} as base

ENV APP_USER=app_user \
    APP_USER_ID=1105 \
    APP_HOME="/opt/app"
ENV MAMBA_NO_LOW_SPEED_LIMIT=1

USER root

RUN groupadd -g ${APP_USER_ID} ${APP_USER} \
  && useradd --create-home --no-log-init -u ${APP_USER_ID} -g ${APP_USER_ID} ${APP_USER}

RUN mkdir -p ${APP_HOME} \
    && chown ${APP_USER}:${APP_USER} ${APP_HOME}

COPY env.yml /tmp/env.yml
RUN micromamba install -y -n base --file /tmp/env.yml && \
    micromamba clean --all --yes

FROM base

# Set working directory
WORKDIR ${APP_HOME}

COPY --chown=${APP_USER}:${APP_USER} src ${APP_HOME}
COPY --chown=${APP_USER}:${APP_USER} pyproject.toml ${APP_HOME}/

RUN chmod -R +r *
RUN /opt/conda/bin/pip install -e ${APP_HOME}

EXPOSE 8050
USER ${APP_USER}
# Run python when the container starts --root_dir /opt/images --host 0.0.0.0
CMD ["python3", "image_search/dash_app.py", "--root_dir", "/opt/images", "--host", "0.0.0.0"]
