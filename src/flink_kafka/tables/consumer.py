from pyflink.table.expressions import col
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment

if __name__ == "__main__":
    env = StreamExecutionEnvironment.get_execution_environment()
    t_env = StreamTableEnvironment.create(stream_execution_environment=env)

    source_ddl = """
      CREATE TABLE kafka_events (
        id INT,
        weight DOUBLE,
        method_name STRING,
        path STRING,
        service STRING
      ) WITH (
        'connector' = 'kafka',
        'topic' = 'api_events',
        'properties.bootstrap.servers' = 'broker:29092',
        'properties.group.id' = 'group0',
        'scan.startup.mode' = 'earliest-offset',
        'format' = 'json'
      )
    """
    t_env.execute_sql(source_ddl)

    sink_ddl = """
      CREATE TABLE results (
        service STRING,
        cnt BIGINT
      ) WITH (
        'connector' = 'print'
      )
    """
    t_env.execute_sql(sink_ddl)

    events = t_env.from_path("kafka_events")
    # events.print_schema()

    events.group_by(col("service")).select(
        col("service"), col("id").count.alias("cnt")
    ).execute_insert("results").wait()
