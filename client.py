# client.py
import sys
import os
sys.path.append('gen-py')

from example import ExampleService
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,

)
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({SERVICE_NAME: "thirft-client"})
))
tracer = trace.get_tracer("thrift-client")

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(
        headers=(("x-honeycomb-team", os.environ.get("HONEYCOMB_API_KEY")),),
        endpoint=os.environ.get("HONEYCOMB_API_ENDPOINT",
                                "https://api.honeycomb.io/v1/traces")
    )))

try:
    # Make socket
    transport = TSocket.TSocket('127.0.0.1', 9090)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = ExampleService.Client(protocol)

    # Connect!
    transport.open()


    with tracer.start_as_current_span("ping") as span:
        span.set_attribute("app.client", True)
        # set the headers to the span context and pass to the server
        headers ={}
        TraceContextTextMapPropagator().inject(headers)
        print(client.ping(headers))
    with tracer.start_as_current_span("sayHello") as span:
        span.set_attribute("app.client", True)
        # set the headers to the span context and pass to the server
        headers ={}
        TraceContextTextMapPropagator().inject(headers)
        print(client.sayHello(headers, "World"))

    # Close!
    transport.close()

except Thrift.TException as tx:
    print(f"%s" % tx.message)
