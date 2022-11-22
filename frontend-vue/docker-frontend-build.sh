#!/usr/bin/env bash

echo "Building to 'dist'"
npm run build

docker build -t quay.io/mechevarria/frontend-vue .

# docker push quay.io/mechevarria/frontend-vue