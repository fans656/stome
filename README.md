# Introduction

Stome is a personal cloud storage implementation.

When deployed on a VPS, you can upload files and download them anywhere.
It supports a file system like structure (e.g. `/img/girl/blue.jpg`).
Also files can be backuped using several third party cloud storages (e.g. Amazon S3).

# Deployment

- Copy/Link `nginx.conf` into `/etc/nginx/sites-enabled/`.
- Run `build.sh`, this will build both frontend and backend, and generate a docker image called "stome-all".
- Run `start.sh`, this will start a docker container using the "stome-all" image.
