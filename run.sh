#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

# Tears down any running containers
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)

# Builds web application image and runs webapp container
TEAMID=`md5sum README.md | cut -d' ' -f 1`
docker build . -t $TEAMID
docker run -p 80:80 -p 8080:8080 -t $TEAMID