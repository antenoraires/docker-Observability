from fastapi import FastAPI
import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter
from opentelemetry.sdk.trace.export import BatchExportSpanProcessor

# Configuração do trace provider e tracer
provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

# Exportador para mostrar os spans no console
exporter = ConsoleSpanExporter()
span_processor = BatchExportSpanProcessor(exporter)
provider.add_span_processor(span_processor)

# Criando o app FastAPI
app = FastAPI()

@app.get("/")
def get_homepage():
    count = 1
    while count <= 3:
        with tracer.start_as_current_span(f"loop-count-{count}") as span:
            print(f"Loop {count}")
            count += 1
            time.sleep(1)  # Simulando uma tarefa demorada
    return {
        "status": "ok",
        "foo": "bar"
    }
