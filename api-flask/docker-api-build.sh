#!/usr/bin/env bash

docker build -t quay.io/mechevarria/api-flask .

docker push quay.io/mechevarria/api-flask