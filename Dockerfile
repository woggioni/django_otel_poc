FROM alpine:latest AS base

RUN --mount=type=cache,target=/var/cache/apk apk update
RUN --mount=type=cache,target=/var/cache/apk apk add python3
RUN adduser -D luser
USER luser
WORKDIR /home/luser

FROM base AS build
RUN python -m venv .venv
#COPY --chown=luser:users --exclude=Dockerfile --exclude=docker-compose.yml . ./django_otel_poc
COPY --chown=luser:users ./requirements-dev.txt ./django_otel_poc/requirements-dev.txt
RUN --mount=type=cache,target=/home/luser/.cache/pip,uid=1000,gid=1000 ~/.venv/bin/pip install -r ./django_otel_poc/requirements-dev.txt

COPY --chown=luser:users ./django_otel_poc ./django_otel_poc/django_otel_poc
COPY --chown=luser:users ./hcms ./django_otel_poc/hcms
COPY --chown=luser:users ./pyproject.toml ./django_otel_poc/pyproject.toml
WORKDIR /home/luser/django_otel_poc
RUN --mount=type=cache,target=/home/luser/.cache/pip,uid=1000,gid=1000 ~/.venv/bin/python -m build

FROM base AS release
RUN python -m venv .venv
RUN --mount=type=cache,target=/home/luser/.cache/pip,uid=1000,gid=1000  .venv/bin/pip install granian
RUN --mount=type=cache,target=/home/luser/.cache/pip,uid=1000,gid=1000 --mount=type=cache,ro,from=build,source=/home/luser/django_otel_poc/dist,target=/home/luser/dist .venv/bin/pip install dist/*.whl
RUN .venv/bin/manage.py collectstatic
ADD scripts/run.sh ./run.sh
ENTRYPOINT ./run.sh

