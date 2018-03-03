#!/usr/bin/python

import json
import os
import datetime
from uuid import uuid4

from flask import Flask, render_template

##########################################
## Set up Flask application
##########################################
views = Flask(__name__)

# TODO: change this to False when submitting
views.config['DEBUG'] = True

# Enable cross origin sharing for all endpoints

# Remember to update this list
ENDPOINT_LIST = ['/',
                '/diary/create_form',
                '/login_form',
                '/register_form',
                '/diary/my_entries']

#############################
## UI Routes
#############################

@views.route('/')
def index():
    return render_template('not_logged_in.html')

@views.route('/diary')
def diary_entries():
    return render_template('diary_index.html')

@views.route('/diary/my_entries')
def diary_my_entries():
    return render_template('my_entries.html')

@views.route('/diary/create_form')
def diary_create_form():
    return render_template('create_entry.html')

@views.route('/login_form')
def users_login_form():
    return render_template('login_form.html')

@views.route('/register_form')
def users_register_form():
    return render_template('register_form.html')

if __name__ == '__main__':
    # Change the working directory to the script directory
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    views.run(debug=False, port=80, host="0.0.0.0")
