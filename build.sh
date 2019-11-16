#!/bin/sh
# Build frontend and backend, generate "stome-all" image.
cd frontend
rm -rf out
docker build -t quantix-frontend .
docker run -d --rm -v $PWD:/data quantix-frontend cp -r /code/out /data/out
cd ..

docker build -t stome-all .
