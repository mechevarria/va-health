#!/usr/bin/env bash
cd ../frontend-vue

echo "Building to 'dist'"
npm run build

docker build -t quay.io/mechevarria/frontend-vue .

# docker push quay.io/mechevarria/frontend-vue