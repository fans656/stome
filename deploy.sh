#!/bin/sh
# Deploy stome service
ssh root@linode 'cd ~/stome && git pull && ./build.sh && ./start.sh'
