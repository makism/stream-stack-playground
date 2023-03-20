#!/bin/bash

docker exec -it broker kafka-console-producer.sh --bootstrap-server localhost:9092 --topic messages
