#!/bin/bash

INFLUXDB_VERSION=2.7.10

# Check these values match .env
INFLUXDB_PORT=8086
INFLUXDB_USERNAME=${INFLUXDB_USERNAME:-puzzlepuzzle}
INFLUXDB_PASSWORD=${INFLUXDB_PASSWORD:-puzzlepuzzle}
INFLUXDB_ORG=${INFLUXDB_ORG:-badaas}
INFLUXDB_BUCKET=${INFLUXDB_BUCKET:-puzzlepuzzle}
INFLUXDB_ADMIN_TOKEN=${INFLUXDB_ADMIN_TOKEN:-puzzlepuzzle}

docker run \
       --name influxdb2 \
       --publish ${INFLUXDB_PORT}:8086 \
       --mount type=volume,source=influxdb2-data,target=/var/lib/influxdb2 \
       --mount type=volume,source=influxdb2-config,target=/etc/influxdb2 \
       --env DOCKER_INFLUXDB_INIT_MODE=setup \
       --env DOCKER_INFLUXDB_INIT_USERNAME=${INFLUXDB_USERNAME} \
       --env DOCKER_INFLUXDB_INIT_PASSWORD=${INFLUXDB_PASSWORD} \
       --env DOCKER_INFLUXDB_INIT_ORG=${INFLUXDB_ORG} \
       --env DOCKER_INFLUXDB_INIT_BUCKET=${INFLUXDB_BUCKET} \
       --env DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=${INFLUXDB_ADMIN_TOKEN} \
       --env DOCKER_INFLUXDB_INIT_RETENTION=0 \
       influxdb:${INFLUXDB_VERSION}
