#!/usr/bin/env bash

# image names from `docker images`
api=quay.io/mechevarria/api-flask
frontend=quay.io/mechevarria/frontend-vue

# remove containers if they exist
docker rm api-flask
docker rm frontend-vue

# remove existing images
docker rmi $api
docker rmi $frontend

echo "loading api.tar"
docker load -i api.tar

echo "loading frontend.tar"
docker load -i frontend.tar

docker images