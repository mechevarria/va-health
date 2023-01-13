#!/usr/bin/env bash

# image names from `docker images`
api=quay.io/mechevarria/api-flask
frontend=quay.io/mechevarria/frontend-vue
repo=../../tar-export


echo "saving $api"
docker save $api -o $repo/api.tar

echo "saving $frontend"
docker save $frontend -o $repo/frontend.tar
