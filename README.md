The repository contains docker-compose files to run a Kafka cluster with different configurations.

---

### 1 - Kafka with Connect & S3 support

This is a docker-compose file to run a Kafka cluster with Connect and S3 (MinIO) support. There's a sample connector that reads from a topic and writes to S3.

```bash
docker-compose -f cp-docker-compose.yml build
docker-compose -f cp-docker-compose.yml up
```

This image is based on the [Confluent All-In-One Images](https://github.com/confluentinc/cp-all-in-one).

#### TODO
* Integrate Flink.

<br/>

### 2 - Kafka and Flink

This is a docker-compose file to run a Kafka cluster with Flink support.

```bash
docker-compose -f kafka-flink.docker-compose.yml build
docker-compose -f kafka-flink.docker-compose.yml up
```

#### Example jobs

##### 1. Read lines
Start the producer and give in some text as input (`src/read_lines/producer.sh`):
```bash
docker exec -it broker kafka-console-producer.sh --bootstrap-server localhost:9092 --topic users
```

At the same time, start a consumer:
```bash
docker exec -it stream-stack-playground_jobmanager_1 flink run -py /opt/src/read_lines/consumer.py
```

###### 2. JSON events

Produce data with:
```bash
python src/flink_kafka/json_events/producer.py --num-events 1000
```

Read the data from Flink with:
```bash
docker exec -it stream-stack-playground_jobmanager_1 flink run -py /opt/src/json_events/consumer.py
```

