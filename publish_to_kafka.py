from typing import List

import json
import time
import random
from uuid import uuid4
from dataclasses import dataclass


from kafka import KafkaProducer


SERVER = "localhost:9094"
TOPIC = "tempo"

trace_id = str(uuid4()).replace("-", "")
root_span_id = str(uuid4()).replace("-", "")[:16]


@dataclass
class Span:
    span_id: str
    name: str
    start_time: int
    end_time: int


def get_spans() -> List[dict]:
    start_time = int(time.time() * 1e9)
    end_time = int(time.time() * 1e9)
    spans = []

    for _ in range(random.randint(0, 5)):
        span_id = str(uuid4()).replace("-", "")[:16]
        name = uuid4().split("-")[0]
        span_start_time = int(time.time() * 1e9)
        end_time += random.randint(0, 7)
        spans.append(Span(span_id=span_id,
                          name=name,
                          start_time=span_start_time,
                          end_time=end_time))

    # root
    name = uuid4().split("-")[0]
    span_start_time = int(time.time() * 1e9)
    spans.append(Span(span_id=root_span_id,
                      name=name,
                      start_time=span_start_time,
                      end_time=end_time))

    return spans

    return {
        "resource": {
            "attributes": [
                {
                    "key": "service.name",
                    "value": {
                        "stringValue": "GET"
                    }
                }
            ]
        },
        "scopeSpans": [
            {
                "spans": [
                    {
                        "traceId": trace_id,
                        "spanId": root_span_id,
                        "name": "GET",
                        "startTimeUnixNano": start_time,
                        "endTimeUnixNano": end_time,
                        "kind": 1,
                        "attributes": [
                            {
                                "key": "systemCode",
                                "value": {
                                    "stringValue": "AAA"
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    }


def publish() -> None:
    producer = KafkaProducer(
        bootstrap_servers=SERVER,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    for i in range(10):
        message = {'message_id': i, 'content': f'This is message {i}'}
        producer.send(TOPIC, value=message)
        print(f'Sent: {message}')
        time.sleep(1)

    producer.close()


if __name__ == "__main__":
    SystemExit(publish())
