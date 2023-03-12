import faker_microservice
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.json_schema import JSONDeserializer, JSONSerializer
from confluent_kafka.serialization import StringSerializer
from faker import Faker

from stream_stack.schemas import SCHEMA_API

fake = Faker()
fake.add_provider(faker_microservice.Provider)


class APIRecord(object):
    def __init__(self, ip: str, method: str, path: str, service: str):
        self.ip = ip
        self.method = method
        self.path = path
        self.service = service


def generate_api_record():
    """Generate a fake API record."""
    return APIRecord(
        ip=fake.ipv4(),
        method=fake.random_element(["GET", "POST", "PUT", "DELETE"]),
        path=fake.uri_path(),
        service=fake.microservice(),
    )


def api_record_to_dict(record, ctx):
    """Convert APIRecord to dict for serialization."""
    return dict(
        ip=record.ip,
        method=record.method,
        path=record.path,
        service=record.service,
    )


def dict_to_api_record(obj, ctx):
    """Convert dict to APIRecord for deserialization."""
    if obj is None:
        return None

    return APIRecord(
        ip=obj.get("ip", ""),
        method=obj.get("method", ""),
        path=obj.get("path", ""),
        service=obj.get("service", ""),
    )


def register_schema():
    """Register the API record schema with the Schema Registry."""
    schema_registry_conf = {"url": "http://localhost:8081"}
    schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    string_serializer = StringSerializer("utf_8")
    json_serializer = JSONSerializer(
        SCHEMA_API, schema_registry_client, api_record_to_dict
    )
    json_deserializer = JSONDeserializer(SCHEMA_API, from_dict=dict_to_api_record)

    return {
        "string": string_serializer,
        "json_ser": json_serializer,
        "json_deser": json_deserializer,
    }


schema_ser = register_schema()
