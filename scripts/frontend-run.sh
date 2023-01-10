#!/usr/bin/env bash

# get the ip address of the api container
API_NAME="api-flask"
API_ID=$(docker ps | grep $API_NAME | cut -d" " -f1)

if [[ -z $API_ID ]]; then
    echo "Could not get docker ID for $API_NAME"
    exit 1
fi

API_ADDRESS=$(docker inspect $API_ID | grep -m1 '"IPAddress": ' | cut -d "\"" -f4)

echo "$API_NAME container IP Address is $API_ADDRESS"

# not using authentication right now
KEYCLOAK=false
KEYCLOAK_URL=http://localhost

docker run \
    --rm \
    -d \
    -p 80:80 \
    --name frontend-vue \
    --env API_ADDRESS=$API_ADDRESS \
    --env KEYCLOAK=$KEYCLOAK \
    --env KEYCLOAK_URL=$KEYCLOAK_URL \
    quay.io/mechevarria/frontend-vue
