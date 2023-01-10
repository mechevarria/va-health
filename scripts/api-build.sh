#!/usr/bin/env bash
cd ../api-flask
docker build -t quay.io/mechevarria/api-flask .

# docker push quay.io/mechevarria/api-flask