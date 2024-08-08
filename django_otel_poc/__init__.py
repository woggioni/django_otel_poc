import os
import sys
from opentelemetry.instrumentation.django import DjangoInstrumentor

def django_manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_otel_poc.dev_settings")
    from django.core.management import execute_from_command_line

    DjangoInstrumentor().instrument()
    execute_from_command_line(sys.argv)