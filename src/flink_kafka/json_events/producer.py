import argparse
import json
import random
import tqdm
import time
from kafka3 import KafkaProducer
from faker import Faker
import faker_microservice


def init_args_parser():
    parser = argparse.ArgumentParser(description="Load and flip an image with OpenCV")
    parser.add_argument(
        "-n",
        "--num-events",
        type=int,
        help="Number of events to emit to the Kafka broker.",
    )

    return parser


def generate_api_event():
    """Generate an API event."""
    return dict(
        id=random.randint(1, 1000),
        weight=random.random(),
        method=fake.random_element(["GET", "POST", "PUT", "DELETE"]),
        path=fake.uri_path(),
        service=fake.microservice(),
    )


if __name__ == "__main__":
    args = init_args_parser().parse_args()

    fake = Faker()
    fake.add_provider(faker_microservice.Provider)

    producer = KafkaProducer(
        # bootstrap_servers="broker:29092", # if run within a pod
        bootstrap_servers="localhost:9092",
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    for ie in tqdm.tqdm(range(args.num_events)):
        time.sleep(random.randrange(1, 3))
        event = generate_api_event()
        producer.send("api_events", generate_api_event())
