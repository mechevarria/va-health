#!/usr/bin/env bash

KEYCLOAK=false
KEYCLOAK_URL=http://localhost

docker rm frontend-vue

docker run \
    -p 80:80 \
    --name frontend-vue \
    --env KEYCLOAK=$KEYCLOAK \
    --env KEYCLOAK_URL=$KEYCLOAK_URL \
    quay.io/mechevarria/frontend-vue
