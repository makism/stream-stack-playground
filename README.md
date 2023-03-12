The repository contains docker-compose files to run a Kafka cluster with different configurations.

---

### 1 - Kafka with Connect & S3 support

This is a docker-compose file to run a Kafka cluster with Connect and S3 (MinIO) support. There's a sample connector that reads from a topic and writes to S3.

```bash
docker-compose -f cp-docker-compose.yml build
docker-compose -f cp-docker-compose.yml up
```

### 2 - Kafka and Flink

This is a docker-compose file to run a Kafka cluster with Flink support.

```bash
docker-compose -f kafka-flink.docker-compose.yml build
docker-compose -f kafka-flink.docker-compose.yml up
```

