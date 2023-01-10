#!/usr/bin/env bash

# image names from `docker images`
api=quay.io/mechevarria/api-flask
frontend=quay.io/mechevarria/frontend-vue

# remove existing images
docker image rm $api
docker image rm $frontend

docker load -i api.tar
docker load -i frontend.tar

docker images