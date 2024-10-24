from typing import List
import json
import time
import random
from uuid import uuid4
from dataclasses import dataclass
from kafka import KafkaProducer

SERVER = "localhost:9094"
TOPIC = "tempo"

trace_id = "AAAAAAAAAAAAAAAAAAAAER=="
root_span_id = "AAAAAAAAAAM="


@dataclass
class Span:
    span_id: str
    name: str
    start_time: int
    end_time: int


def get_spans() -> List[Span]:
    start_time = int(time.time() * 1e9)
    end_time = start_time
    spans = []

    for _ in range(random.randint(0, 5)):
        span_id = str(uuid4()).replace("-", "")[:16]
        name = str(uuid4()).split("-")[0]
        span_start_time = end_time
        span_end_time = span_start_time + random.randint(0, 7) * int(1e9)
        spans.append(Span(span_id=span_id,
                          name=name,
                          start_time=span_start_time,
                          end_time=span_end_time))
        end_time = span_end_time

    name = str(uuid4()).split("-")[0]
    spans.append(Span(span_id=root_span_id,
                      name=name,
                      start_time=start_time,
                      end_time=end_time))

    return spans


def publish() -> None:
    producer = KafkaProducer(
        bootstrap_servers=SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    spans = get_spans()
    spans, root = spans[:-1], spans[-1]

    root_data = {
        "traceId": trace_id,
        "spanId": root_span_id,
        "operationName": "example-operation-1",
        "references": [],
        "startTime": root.start_time,
        "duration": "10ns",
        "tags": [],
        "process": {
            "serviceName": "example-service-1",
            "tags": []
        },
        "logs": [
            {
                "timestamp": root.start_time,
                "fields": []
            },
        ]
    }

    producer.send(TOPIC, value=root_data)
    producer.close()


if __name__ == "__main__":
    SystemExit(publish())
