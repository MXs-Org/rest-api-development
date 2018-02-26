#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

#Apache2 might run on the same port, just kill it
ps auxw | grep apache2 | grep -v grep > /dev/null

if [ $? == 0 ]
then
        /etc/init.d/apache2 stop > /dev/null
fi

ps auxw | grep mysql | grep -v grep > /dev/null

if [ $? == 0 ]
then
        service mysql stop > /dev/null
fi

TEAMID=`md5sum README.md | cut -d' ' -f 1`
docker kill $(docker ps -q)
docker rm $(docker ps -a -q)

docker pull mysql

docker build . -t $TEAMID

echo "Starting app and database"

docker run -v /var/lib/mysql --name=testsql -e MYSQL_ROOT_PASSWORD=password -d mysql

echo "Loading Database"
sleep 30

docker run -p 80:80 -p 8080:8080 --link=testsql -t $TEAMID