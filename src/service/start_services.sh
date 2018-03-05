#!/bin/bash

# This script is executed WITHIN the Docker container
# Everything in the /src/service folder is now found in /service of the container
# Everything in the /src/html folder is now found in /var/www/html of the container

# Start the Flask application
python /service/app.py &
python /service/views.py