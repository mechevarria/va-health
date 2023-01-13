#!/usr/bin/env bash

# image names from `docker images`
api=quay.io/mechevarria/api-flask
frontend=quay.io/mechevarria/frontend-vue

echo "saving $api"
docker save $api -o ../export/api.tar

echo "saving $frontend"
docker save $frontend -o ../export/frontend.tar
