from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment
from pyflink.table import Schema, DataTypes
from pyflink.datastream.connectors.kafka import KafkaSource
from pyflink.datastream.formats.json import JsonRowDeserializationSchema
from pyflink.common.typeinfo import Types
from pyflink.common.watermark_strategy import WatermarkStrategy

if __name__ == "__main__":
    env = StreamExecutionEnvironment.get_execution_environment()
    table_env = StreamTableEnvironment.create(stream_execution_environment=env)

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

    schema = (
        Schema.new_builder()
        .column("id", DataTypes.INT())
        .column("weight", DataTypes.DOUBLE())
        .column("method", DataTypes.STRING())
        .column("path", DataTypes.STRING())
        .column("service", DataTypes.STRING())
        .build()
    )

    t = table_env.from_data_stream(ds, schema)
    table_env.create_temporary_view("api_events", t)

    res_table = table_env.sql_query(
        """
        SELECT
            service,
            SUM(weight) AS total_weight
        FROM api_events
        GROUP BY service
    """
    )
    # res_ds = table_env.to_data_stream(res_table)
    # res_ds.print()

    res_table.execute().print()

    env.execute()
