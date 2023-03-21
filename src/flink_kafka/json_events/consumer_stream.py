from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy

if __name__ == "__main__":
    env = StreamExecutionEnvironment.get_execution_environment()
    type_info = Types.ROW_NAMED(
        ["id", "weight", "method", "path", "service"],
        [
            Types.INT(),
            Types.DOUBLE(),
            Types.STRING(),
            Types.STRING(),
            Types.STRING(),
        ],
    )
    ser_schema = JsonRowDeserializationSchema.builder().type_info(type_info).build()

    kafka_consumer = (
        KafkaSource.builder()
        .set_bootstrap_servers("broker:29092")
        .set_topics("api_events")
        .set_group_id("api_events")
        .set_value_only_deserializer(ser_schema)
        .build()
    )

    ds = env.from_source(
        source=kafka_consumer,
        watermark_strategy=WatermarkStrategy.for_monotonous_timestamps(),
        source_name="kafka source",
    )

    ms = (
        ds.map(lambda row: (row.id, row.weight))
        .key_by(lambda row: row[0])
        .sum(1)
    )
    ms.print()

    env.execute()
