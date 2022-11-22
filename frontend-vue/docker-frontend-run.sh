#!/usr/bin/env bash

# not using authentication right now
KEYCLOAK=false
KEYCLOAK_URL=http://localhost

# create network for other containers to communicate via name
docker network create app-net

docker run \
    --rm \
    -d \
    -p 80:80 \
    --name frontend-vue \
    --network app-net \
    --env KEYCLOAK=$KEYCLOAK \
    --env KEYCLOAK_URL=$KEYCLOAK_URL \
    quay.io/mechevarria/frontend-vue
