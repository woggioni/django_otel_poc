#!/usr/bin/env sh
.venv/bin/manage.py migrate
exec .venv/bin/granian $@ django_otel_poc.asgi:application