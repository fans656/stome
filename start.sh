#!/bin/sh
# Start stome service
NAME=stome-all
docker stop $NAME
docker run -d --rm \
    -p 4431:80 \
    --name $NAME \
    $NAME
