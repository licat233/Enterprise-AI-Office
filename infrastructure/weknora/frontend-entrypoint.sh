#!/bin/sh
set -eu

template=/etc/nginx/templates/default.conf.template
upstream_entrypoint=/docker-entrypoint.sh

[ -f "$template" ] || {
  echo "EAO: missing WeKnora nginx template: $template" >&2
  exit 1
}

[ -x "$upstream_entrypoint" ] || {
  echo "EAO: missing upstream frontend entrypoint: $upstream_entrypoint" >&2
  exit 1
}

proxy_count=$(grep -c 'proxy_pass ${APP_SCHEME}://${APP_HOST}:${APP_PORT}' "$template" || true)
[ "$proxy_count" -eq 4 ] || {
  echo "EAO: unsupported WeKnora nginx template: expected 4 app proxy_pass entries, found $proxy_count" >&2
  exit 1
}

server_count=$(grep -c '^[[:space:]]*server_name localhost;' "$template" || true)
[ "$server_count" -eq 1 ] || {
  echo "EAO: unsupported WeKnora nginx template: expected one localhost server block" >&2
  exit 1
}

cp "$template" /tmp/eao-default.conf.template

sed -i '/^[[:space:]]*server_name localhost;/a\
    # EAO: Docker service IPs are ephemeral; resolve app through embedded DNS.\
    resolver 127.0.0.11 valid=10s ipv6=off;\
    set $weknora_backend ${APP_HOST}:${APP_PORT};
' /tmp/eao-default.conf.template

sed -i \
  -e 's#proxy_pass ${APP_SCHEME}://${APP_HOST}:${APP_PORT}/files;#proxy_pass ${APP_SCHEME}://$weknora_backend$request_uri;#g' \
  -e 's#proxy_pass ${APP_SCHEME}://${APP_HOST}:${APP_PORT}/api/;#proxy_pass ${APP_SCHEME}://$weknora_backend$request_uri;#g' \
  -e 's#proxy_pass ${APP_SCHEME}://${APP_HOST}:${APP_PORT};#proxy_pass ${APP_SCHEME}://$weknora_backend$request_uri;#g' \
  /tmp/eao-default.conf.template

post_count=$(grep -c 'proxy_pass ${APP_SCHEME}://$weknora_backend$request_uri;' /tmp/eao-default.conf.template || true)
[ "$post_count" -eq 4 ] || {
  echo "EAO: nginx template patch failed: expected 4 dynamic proxy entries, found $post_count" >&2
  exit 1
}

cp /tmp/eao-default.conf.template "$template"
exec "$upstream_entrypoint"
