#!/usr/bin/python

import json
import os

from flask_sqlalchemy import SQLAlchemy
from database import db
from flask import Flask, request
from flask_cors import CORS

from models import User

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
ENDPOINT_LIST = ['/', '/meta/heartbeat', '/meta/members', '/diary', '/diary/create', '/diary/delete', 'diary/permission']

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

def verify_user_registration(request):
    # Checks if registration fields are all filled in
    if len(request.form) < 4:
        import pdb; pdb.set_trace()
        return False
    elif (request.form['username'] and request.form['password'] 
        and request.form['fullname'] and request.form['age']):
        return True
    return False

#############################
## Admin Routes
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

#############################
## Users Routes
#############################

@app.route("/users/register", methods=['POST'])
def register_user():
    if request.method == 'POST':
        if not verify_user_registration(request):
            return make_json_response("Please fill in all the required information", False)
        try:
            user = User(username=request.form['username'], fullname=request.form['fullname'], age=request.form['age'])
            user.set_password(request.form['password'])
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            return make_json_response("User already exists!", False)
        return make_json_response(None)

@app.route("/users/authenticate", methods=['POST'])
def auth_user():
    pass

@app.route("/users/expire", methods=['POST'])
def expire_token():
    pass

@app.route("/users", methods=['POST'])
def retrieve_user_info():
    pass

#############################
## Diary Routes
#############################

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if request.method == 'GET':
        # TODO retrieve all public entries
        return "get /diary"
    else:
        # TODO retrieve all entries of authenicated user
        return "post /diary"

@app.route('/diary/create', methods=['POST'])
def diary_create():
    # TODO create a new diary entry
    return "create!"

@app.route('/diary/delete', methods=['POST'])
def diary_delete():
    # TODO delete an existing diary entry
    return "delete!"

@app.route('/diary/permission', methods=['POST'])
def diary_permission():
    # TODO change permission of diary entry
    return "change permissions!"

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
