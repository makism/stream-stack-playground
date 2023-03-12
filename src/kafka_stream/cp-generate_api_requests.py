import sys
from uuid import uuid4
from random import randint
from time import sleep
import datetime

from confluent_kafka import Producer, KafkaException
from confluent_kafka import Producer
from confluent_kafka.serialization import (
    SerializationContext,
    MessageField,
)

from tqdm import tqdm

from stream_stack.utils import delivery_report
from stream_stack.producers.api import schema_ser, generate_api_record

if __name__ == "__main__":
    NUM_MESSAGES = 1000
    TOPIC = "api_requests"
    TIMESTAMP = int(datetime.datetime(2012, 4, 1, 0, 0).timestamp())

    conf = {"bootstrap.servers": "localhost:9092"}
    p = Producer(**conf)

    string_ser, json_ser = schema_ser["string"], schema_ser["json_ser"]

    for i in tqdm(range(NUM_MESSAGES)):
        delay = randint(1, 3)
        sleep(delay)

        api_record = generate_api_record()

        p.poll(0.0)
        try:
            p.produce(
                topic=TOPIC,
                key=string_ser(str(uuid4())),
                value=json_ser(
                    api_record, SerializationContext(TOPIC, MessageField.VALUE)
                ),
                # timestamp=TIMESTAMP,
                on_delivery=delivery_report,
            )
        except KafkaException as kafka_err:
            sys.stderr.write(kafka_err)
        except BufferError:
            sys.stderr.write(
                "%% Local producer queue is full (%d messages awaiting delivery): try again\n"
                % len(p)
            )

        p.flush()
