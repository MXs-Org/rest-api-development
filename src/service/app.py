#!/usr/bin/python

import json
import os
import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template
from flask_cors import CORS

from database import db
from models import User, Token, Entry

##########################################
## Set up Flask application and database
##########################################
app = Flask(__name__)
# TODO: change this to False when submitting
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Enable cross origin sharing for all endpoints
CORS(app)
db.init_app(app)

# Remember to update this list
ENDPOINT_LIST = ['/',
                '/meta/heartbeat',
                '/meta/members',
                '/users/register',
                '/users/authenticate',
                '/users/expire',
                '/users',
                '/users/check',
                '/diary',
                '/diary/create',
                '/diary/delete',
                '/diary/permission']

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

def make_json_false_response():
    # Helper function just to return False, since it's not handled by
    # make_json_response, which requires an explicit Error message
    response = app.response_class(
        response=json.dumps({'status': False}),
        status=200,
        mimetype='application/json'
    )
    return response

def add_user_token():
    # Creates a fresh UUID and stores it in the database
    # If a token for a user_id already exists, return the existing token
    req_data = request.get_json()
    user_id = User.query.filter_by(username=req_data['username']).first().id
    user_token = Token.query.filter_by(user_id=user_id).first()
    if user_token:
        return user_token.token
    else:
        new_uuid = str(uuid4())
        token = Token(token=new_uuid, user_id=user_id)
        db.session.add(token)
        db.session.commit()
        return new_uuid

def remove_user_token(token_str):
    # Removes the token from Token table
    token = Token.query.filter_by(token=token_str).first()
    db.session.delete(token)
    db.session.commit()

def check_valid_token(token_str):
    # Checks if the token is valid
    token = Token.query.filter_by(token=token_str).first()
    return bool(token)

def retrieve_user_id(token_str):
    # Returns the user_id of the user who currently owns token_str
    token = Token.query.filter_by(token=token_str).first()
    user_id = token.user_id
    return user_id

def create_diary_entry(req_data):
    # Gets attributes of entry
    title = req_data['title']
    user_id = retrieve_user_id(req_data['token'])
    publish_date = datetime.datetime.utcnow().isoformat()
    public = req_data['public']
    text = req_data['text']
    # Adds entry to database
    entry = Entry(title=title, user_id=user_id, publish_date=publish_date,
                    public=public, text=text)
    db.session.add(entry)
    db.session.commit()
    return entry.id

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
        req_data = request.get_json()
        if not all(k in req_data.keys() for k in ['username', 'password', 'fullname', 'age']):
            return make_json_response("Please fill in all the required information", False)
        try:
            user = User(username=req_data['username'],
                        fullname=req_data['fullname'],
                        age=req_data['age'])
            user.set_password(req_data['password'])
            db.session.add(user)
            db.session.commit()
        except:
            return make_json_response("User already exists!", False)
        return make_json_response(None, code=201)

@app.route("/users/authenticate", methods=['POST'])
def auth_user():
    req_data = request.get_json()
    if not all(k in req_data.keys() for k in ['username', 'password']):
        return make_json_response("Please fill in all the required information", False)
    auth_user = User.query.filter_by(username=req_data['username']).first()
    if auth_user:
        if auth_user.check_password(req_data['password']):
            token = add_user_token()
            return make_json_response({"token": token})
    return make_json_false_response()

@app.route("/users/expire", methods=['POST'])
def expire_token():
    req_data = request.get_json()
    if req_data['token']:
        token = Token.query.filter_by(token=req_data['token']).first()
        if token:
            token_str = token.token
            remove_user_token(token_str)
            return make_json_response(None)
    return make_json_false_response()

@app.route("/users", methods=['POST'])
def retrieve_user_info():
    req_data = request.get_json()
    if req_data['token']:
        token = Token.query.filter_by(token=req_data['token']).first()
        if token:
            user_id = token.user_id
            user = User.query.filter_by(id=user_id).first()
            return make_json_response(user.json_dict())
    return make_json_response("Invalid authentication token.", False)

@app.route("/users/check", methods=['POST'])
def retrieve_token_validity():
    req_data = request.get_json()
    if req_data['token']:
        token = Token.query.filter_by(token=req_data['token']).first()
        if token:
            return make_json_response(None)
    return make_json_false_response()

#############################
## Diary Routes
#############################

@app.route('/diary', methods=['GET', 'POST'])
def diary():
    if request.method == 'GET':
        entries = Entry.query.filter_by(public=True).all()
        return make_json_response([e.json_dict() for e in entries])
    else:
        req_data = request.get_json()
        if check_valid_token(req_data['token']):
            user_id = retrieve_user_id(req_data['token'])
            entries = Entry.query.filter_by(user_id=user_id).all()
            return make_json_response([e.json_dict() for e in entries])
        return make_json_response("Invalid authentication token.", False)

@app.route('/diary/create', methods=['POST'])
def diary_create():
    req_data = request.get_json()
    if not all(k in req_data.keys() for k in ['token', 'title', 'public', 'text']):
        return make_json_response("Invalid authentication token.", False)
    # Check if token is valid
    if check_valid_token(req_data['token']):
        entry_id = create_diary_entry(req_data)
        return make_json_response({'id': entry_id}, status=201)
    return make_json_response("Invalid authentication token.", False)

@app.route('/diary/delete', methods=['POST'])
def diary_delete():
    req_data = request.get_json()
    if not all(k in req_data.keys() for k in ['token', 'id']):
        return make_json_response("Invalid authentication token.", False)
    if not check_valid_token(req_data['token']):
        return make_json_response("Invalid authentication token.", False)

    entry = Entry.query.get(req_data['id'])
    if entry is None:
         return make_json_response("Entry does not exist.", False)

    req_user_id = retrieve_user_id(req_data['token'])
    if entry.user_id != req_user_id: # only owner of entry can delete entry
        return make_json_response("Invalid authentication token.", False)

    db.session.delete(entry)
    db.session.commit()

    return make_json_response(None)

@app.route('/diary/permission', methods=['POST'])
def diary_permission():
    req_data = request.get_json()
    if not all(k in req_data.keys() for k in ['token', 'id', 'public']):
        return make_json_response("Invalid authentication token.", False)
    if not check_valid_token(req_data['token']):
        return make_json_response("Invalid authentication token.", False)

    entry = Entry.query.get(req_data['id'])
    if entry is None:
         return make_json_response("Entry does not exist.", False)

    req_user_id = retrieve_user_id(req_data['token'])
    if entry.user_id != req_user_id: # only owner of entry can change the permission
        return make_json_response("Invalid authentication token.", False)

    entry.public = req_data['public']
    db.session.commit()
    return make_json_response(None)

if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # If sqlite database does not exist, create it
    if not os.path.isfile('/tmp/test.db'):
        setup_database(app)
    app.run(debug=False, port=8080, host="0.0.0.0")
