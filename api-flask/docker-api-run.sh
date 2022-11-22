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
    quay.io/mechevarria/api-flask
