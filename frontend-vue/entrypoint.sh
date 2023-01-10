#!/usr/bin/env bash

set -e

envsubst < /usr/share/nginx/html/js/env.template.js > /usr/share/nginx/html/js/env.js
envsubst '${API_ADDRESS}' < /tmp/default.template.conf > /etc/nginx/conf.d/default.conf

exec "$@"