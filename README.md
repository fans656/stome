# Introduction

Stome is a personal cloud storage implementation.

Features:
- Upload/Download files (of course)
- File system like structure (e.g. `/img/girl/blue.jpg`)
- Backup using 3rd-party cloud storages (e.g. Amazon S3)

# Deployment

- Copy `nginx.conf` into `/etc/nginx/sites-enabled/`.
- Run `build.sh`, this will build both frontend and backend, and generate a docker image called "stome-all".
- Run `start.sh`, this will start a docker container using the "stome-all" image.
