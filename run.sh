#!/bin/bash

if [ "$EUID" -ne 0 ]
    then echo "Please run as root"
    exit
fi

# Apache2 might run on the same port, just kill it
ps auxw | grep apache2 | grep -v grep > /dev/null

if [ $? == 0 ]
then
    /etc/init.d/apache2 stop > /dev/null
fi

# Kill any running mysql first
ps auxw | grep mysql | grep -v grep > /dev/null

if [ $? == 0 ]
then
    service mysql stop > /dev/null
fi

# Tears down any running containers
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)

# Prepare database directory
mkdir -p /tmp/diary_db

# Pull mysql image and runs MySQL container
docker pull mysql
echo "Starting app and database"
docker run -v /tmp/diary_db:/var/lib/mysql --name=diary_db_container -e MYSQL_ROOT_PASSWORD=password -d mysql
echo "Loading Database"
sleep 5

# Creates the database "diary_db"
# TODO: add code here to automate the creation of the MySQL database

# Builds web application image and runs webapp container
TEAMID=`md5sum README.md | cut -d' ' -f 1`
docker build . -t $TEAMID
docker run -p 80:80 -p 8080:8080 --link=diary_db_container -t $TEAMID