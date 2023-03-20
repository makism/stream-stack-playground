from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import SimpleStringSchema
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
from pyflink.datastream import StreamExecutionEnvironment

if __name__ == "__main__":
    env = StreamExecutionEnvironment.get_execution_environment()

    deserialization_schema = SimpleStringSchema()

    kafka_consumer = FlinkKafkaConsumer(
        topics="users",
        deserialization_schema=deserialization_schema,
        properties={"bootstrap.servers": "broker:29092", "group.id": "users"},
    )

    ds = env.add_source(kafka_consumer)
    ds.print()

    env.execute()
