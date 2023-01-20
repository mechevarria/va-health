#!/usr/bin/env bash

# read in environment
env_path=../api-flask/.env
if [[ ! -f $env_path ]]; then
    env_path=.env
fi

echo "Setting environment from $env_path"
source $env_path

docker rm api-flask

docker run \
    -d \
    -p 5000:5000 \
    --name api-flask \
    --env AYASDI_APISERVER=$AYASDI_APISERVER \
    --env EUREKA_USER=$EUREKA_USER \
    --env EUREKA_PASS=$EUREKA_PASS \
    --env SOURCE_NAME=$SOURCE_NAME \
    --env SOURCE_NAME_HOLDOUT=$SOURCE_NAME_HOLDOUT \
    --env FLASK_APP=$FLASK_APP \
    --env FLASK_DEBUG=$FLASK_DEBUG \
    --env NETWORK_NAME=$NETWORK_NAME \
    quay.io/mechevarria/api-flask
