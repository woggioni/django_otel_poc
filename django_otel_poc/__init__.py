import os
import sys
from .instrumentation import setup as setup_instrumentation

def django_manage():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_otel_poc.dev_settings")
    enable_otel_instrumentation = os.environ.get("OTEL_INSTRUMENTATION", "False")
    if enable_otel_instrumentation and enable_otel_instrumentation.lower() == 'true':
        setup_instrumentation()
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
