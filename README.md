
# Spin

Star tthe cluster with
```bash
docker-compose up
```

## Create the connector

The connector is created using the following command:
```bash
docker-compose run exec -it connect-cli create kafka-to-s3-connector < /kafka-connectors/kafka-to-s3-connector.properties
```
