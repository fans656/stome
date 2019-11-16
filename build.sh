#!/bin/sh
# Build frontend and backend, generate "stome-all" image.
cd frontend
rm -rf out
docker build -t stome-frontend .
docker run -d --rm -v $PWD:/data stome-frontend cp -r /code/out /data/out
cd ..

docker build -t stome-all .
