#!/bin/bash

set -ue

IMAGE={{ docker_image }}:{{ docker_tag }}

docker run \
    -d \
    --name={{ container_name }} \
    --restart always \
    ${IMAGE}