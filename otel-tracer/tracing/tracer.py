from flask import request
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.pika import PikaInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

servicename = "do-host-operations"
endpoint = "http://otel-collector.helium.svc.cluster.local:4317"


def flask_tracer(app, servicename, endpoint):
    FlaskInstrumentor().instrument_app(app)

    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({"service.name": servicename})
        )
    )

    otlp_exporter = OTLPSpanExporter(
        endpoint=endpoint  # Use the address and port of your OpenTelemetry Collector
    )
    span_processor = BatchSpanProcessor(otlp_exporter)

    trace.get_tracer_provider().add_span_processor(span_processor)

    @app.before_request
    def start_span():
        span_name = request.path or "root"
        request.span = trace.get_tracer(__name__).start_span(span_name)

    @app.after_request
    def end_span(response):
        request.span.end()
        return response
    return app


def requests_tracer():
    RequestsInstrumentor().instrument()


def redis_tracer():
    RedisInstrumentor().instrument()


def pika_tracer():
    PikaInstrumentor().instrument()


def celery_tracer():
    pass


def flask_sqlalchemy_tracer():
    SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})
