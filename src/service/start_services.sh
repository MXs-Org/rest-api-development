#!/bin/bash

# This script is executed WITHIN the Docker container
# Everything in the /src/service folder is now found in /service of the container
# Everything in the /src/html folder is now found in /var/www/html of the container

# Start the apache server to serve files over port 80
apachectl start

# Start the Flask application
python /service/app.py
