from flask import Flask, render_template, request, make_response
import sqlite3
import random
from flask_httpauth import HTTPBasicAuth # https://flask-httpauth.readthedocs.io/en/latest/

app = Flask(__name__)

@app.route('/users/<user>/public')
def handle(user):
    return "<h1>this is your public profile <img src=internal/profile.png>"

@app.route('/users/<user>/internal')
def handle(user):
    return "here is your private info, {}: CREDIT CARD: 5243-3213-5455-{} cvv: 777".format(user, user)
