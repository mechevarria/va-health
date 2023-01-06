#!/usr/bin/env bash

# create network for other containers to communicate via name
docker network create app-net

# read in environment
source .env

docker run \
    --rm \
    -d \
    -p 5000:5000 \
    --network app-net \
    --name api-flask \
    --env AYASDI_APISERVER=$AYASDI_APISERVER \
    --env EUREKA_USER=$EUREKA_USER \
    --env EUREKA_PASS=$EUREKA_PASS \
    --env SOURCE_NAME=$SOURCE_NAME \
    --env SOURCE_NAME_HOLDOUT=$SOURCE_NAME_HOLDOUT \
    --env FLASK_APP=$FLASK_APP \
    --env FLASK_DEBUG=$FLASK_DEBUG \
    quay.io/mechevarria/api-flask
