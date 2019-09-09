#!/bin/sh
# Build frontend assets inside a docker container and copy results into ./out/
IMAGE="stome-frontend"
rm -rf out
docker build -t $IMAGE .
docker run -d --rm -v $PWD:/data $IMAGE cp -r /code/out /data/out
