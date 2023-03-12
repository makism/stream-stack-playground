from confluent_kafka import Consumer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)

from stream_stack.logger import logger
from stream_stack.utils import on_assign_cb
from stream_stack.producers.api import schema_ser


if __name__ == "__main__":
    topics = [
        "api_requests",
    ]
    conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "group0",
        "session.timeout.ms": 6000,
        "auto.offset.reset": "earliest",
        "enable.auto.offset.store": False,
    }

    c = Consumer(conf, logger=logger)
    c.subscribe(topics, on_assign=on_assign_cb)

    string_ser, json_deser = schema_ser["string"], schema_ser["json_deser"]

    while True:
        try:
            msg = c.poll(1.0)
            if msg is None:
                continue

            api_record = json_deser(
                msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)
            )

            if api_record is not None:
                c.store_offsets(msg)

                print(
                    f"""
    - key: {msg.key()}
    - ts: {msg.timestamp()}
    - value:
        ip: {api_record.ip}
        method: {api_record.method}
        path: {api_record.path}
        service: {api_record.service}
                """
                )

        except KeyboardInterrupt:
            break

    c.close()
