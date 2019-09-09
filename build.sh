#!/bin/sh
# Build frontend and backend, generate "stome-all" image.
cd frontend && ./build.sh
cd .. && docker build -t stome-all .
