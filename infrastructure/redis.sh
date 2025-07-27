#!/bin/bash

DOCKER_IMAGE_VERSION=8.0
# Check this match the value in .env
REDIS_PORT=${REDIS_PORT:-6379}

docker run \
       --name redis \
       -v "$(pwd)"/redis-data:/data \
       --publish "${REDIS_PORT}":6379 \
       redis:"${DOCKER_IMAGE_VERSION}" \
       redis-server \
       --save 60 1 \
       --loglevel warning
