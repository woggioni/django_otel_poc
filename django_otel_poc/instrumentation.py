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
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import LogExporter, BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
)
from opentelemetry.metrics import set_meter_provider
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
from opentelemetry.instrumentation.django import DjangoInstrumentor
from  opentelemetry.instrumentation.logging import LoggingInstrumentor
import os
from logging import getLogger
import logging

def setup():
    resource = Resource(
        attributes={
            ResourceAttributes.SERVICE_NAME: 'hcms',
            ResourceAttributes.SERVICE_INSTANCE_ID: os.uname().nodename,
        }
    )

    if settings.DEBUG:
        span_exporter = OTLPSpanExporter(
            endpoint='http://127.0.0.1:8200',
            insecure=True
        )
        metric_exporter = OTLPMetricExporter(
            endpoint='http://127.0.0.1:8200',
            insecure=True
        )
        log_exporter = OTLPLogExporter(
            endpoint='http://127.0.0.1:8200',
            insecure=True
        )
    else:
        span_exporter = OTLPSpanExporter()
        metric_exporter = OTLPMetricExporter()
        log_exporter = OTLPLogExporter()

    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    _logs.set_logger_provider(logger_provider)
    # handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)

    tracer_provider: TracerProvider = TracerProvider(
        resource=resource
    )
    tracer_provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(tracer_provider)

    reader = PeriodicExportingMetricReader(metric_exporter)
    meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(meterProvider)

    DjangoInstrumentor().instrument()
    # to configure custom metrics
    # configuration = {
    #     "system.memory.usage": ["used", "free", "cached"],
    #     "system.cpu.time": ["idle", "user", "system", "irq"],
    #     "system.network.io": ["transmit", "receive"],
    #     "process.runtime.memory": ["rss", "vms"],
    #     "process.runtime.cpu.time": ["user", "system"],
    #     "process.runtime.context_switches": ["involuntary", "voluntary"],
    # }
    SystemMetricsInstrumentor().instrument()
    # LoggingInstrumentor(log_level=logging.DEBUG).instrument()