from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

app = Flask(__name__)

users = {
    "john": generate_password_hash("bryce"),
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
    response=make_response("welcome <img src=public/logo.png>")
    response.set_cookie('cookie', cookie)
    return redirect("/users/{}/public".format(auth.current_user()))
    #return response

@app.route('/users/<user>/public')
def public(user):
    print(user)
    return "<h1>this is your public profile <img src=internal/profile.png>"

@app.route('/users/<user>/internal')
def internal(user):
    return "here are your secrets, {}: CREDIT CARD: 5243-3213-5455-{} cvv: 777".format(user, user)
