from django.conf import settings
from opentelemetry import trace, metrics, _logs
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader, ConsoleMetricExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.resources import ResourceAttributes
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)
from opentelemetry.sdk._logs.export import LogExporter, BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)

_logs.Logger
from logging import getLogger

resource = Resource(
    attributes={
        ResourceAttributes.SERVICE_NAME: 'hcms'
    }
)

trace.set_tracer_provider(TracerProvider(resource=resource))

if settings.DEBUG:
    span_exporter = OTLPSpanExporter(
        endpoint='http://127.0.0.1:4317',
        insecure=True
    )
    metric_exporter = OTLPMetricExporter(
        endpoint='http://127.0.0.1:4317',
        insecure=True
    )
else:
    span_exporter = OTLPSpanExporter()
    metric_exporter = OTLPMetricExporter()

tracer_provider: TracerProvider = trace.get_tracer_provider()
tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
reader = PeriodicExportingMetricReader(metric_exporter)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)

