from flask import Flask, render_template, request, make_response
from flask_httpauth import HTTPBasicAuth # https://flask-httpauth.readthedocs.io/en/latest/
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import random

app = Flask(__name__)
auth = HTTPBasicAuth()
users = {
    "tal": generate_password_hash("tal123"),
    "moshe": generate_password_hash("moshe123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    return False

@app.route('/login')
@auth.login_required
def login():
    cookie=str(random.randint(1000, 9999))
    response=make_response("welcome")
    response.set_cookie('cookie', cookie)
    return response

@app.route('/users/<user>/internal')
@auth.login_required
def handle(user):
    return "here are your secrets, {}: CREDIT CARD: 5243-3213-5455-{} cvv: 777".format(user, user)
