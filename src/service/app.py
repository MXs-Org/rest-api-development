#!/usr/bin/python

from flask_sqlalchemy import SQLAlchemy
from database import db
from flask import Flask
from flask_cors import CORS
from models import User
import json
import os

##########################################
## Set up Flask application and database
##########################################
app = Flask(__name__)
app.config['DEBUG'] = True
# TODO: migrate to MySQL after development is done, or maybe not?
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/diary_db'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Enable cross origin sharing for all endpoints
CORS(app)
db.init_app(app)

# Remember to update this list
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members']

#############################
## Helper functions
#############################

def setup_database(app):
    with app.app_context():
        db.create_all()

def make_json_response(data, status=True, code=200):
    """Utility function to create the JSON responses."""

    to_serialize = {}
    if status:
        to_serialize['status'] = True
        if data is not None:
            to_serialize['result'] = data
    else:
        to_serialize['status'] = False
        to_serialize['error'] = data
    response = app.response_class(
        response=json.dumps(to_serialize),
        status=code,
        mimetype='application/json'
    )
    return response

#############################
## Routes
#############################

@app.route("/")
def index():
    """Returns a list of implemented endpoints."""
    return make_json_response(ENDPOINT_LIST)


@app.route("/meta/heartbeat")
def meta_heartbeat():
    """Returns true"""
    return make_json_response(None)


@app.route("/meta/members")
def meta_members():
    """Returns a list of team members"""
    with open("./team_members.txt") as f:
        team_members = f.read().strip().split("\n")
    return make_json_response(team_members)


if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Checks if the sqlite database already exists
    # TODO: need to change this when we move back to MySQL
    if not os.path.isfile('/tmp/test.db'):
      setup_database(app)
    app.run(debug=False, port=8080, host="0.0.0.0")
