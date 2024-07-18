# server.py
import sys
import os
from time import sleep
sys.path.append('gen-py')

from example import ExampleService
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# OpenTelemetry
from opentelemetry import trace
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({SERVICE_NAME: "thirft-server"})
))
tracer = trace.get_tracer("thrift-server")

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(
        headers=(("x-honeycomb-team", os.environ.get("HONEYCOMB_API_KEY")),),
        endpoint=os.environ.get("HONEYCOMB_API_ENDPOINT",
                                "https://api.honeycomb.io/v1/traces")
    )))

class ExampleHandler:
    def ping(self, headers):
        # set the context from the headers and start a span with that context
        ctx = TraceContextTextMapPropagator().extract(carrier=headers)
        with tracer.start_as_current_span("pong", context=ctx) as span:
            print(f"ping()")
        return "pong"

    def sayHello(self, headers, name):
        # set the context from the headers and start a span with that context
        ctx = TraceContextTextMapPropagator().extract(carrier=headers)
        with tracer.start_as_current_span("sayHello", context=ctx) as span:
            span.set_attribute("app.name", name)
            span.set_attribute("app.server", True)
            sleep(1)
            print(f"sayHello({name})")
        return f"Hello, {name}"

if __name__ == "__main__":
    handler = ExampleHandler()
    processor = ExampleService.Processor(handler)
    transport = TSocket.TServerSocket(host='127.0.0.1', port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
    print("Starting the server...")
    server.serve()
    print("done.")
