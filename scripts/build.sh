#!/usr/bin/env bash
set -ex
# Build SPA
(cd 'single-page-frontend' && npm install && npm run build)
mv single-page-frontend/build/*{.html,.json,.js} frontend/frontend/static/
rm -rf frontend/frontend/static/js/*
mv single-page-frontend/build/static/js/*.js frontend/frontend/static/js/

# Build docker images
IMAGE_PREFIX='brettlangdon/distributed-tracing-workshop-'
for app in 'frontend' 'node-api' 'pumps-api' 'sensors';
do
    echo "Building docker image for ${app}"
    docker build -t "${IMAGE_PREFIX}${app}" "./${app}"
    docker push "${IMAGE_PREFIX}${app}"
done
