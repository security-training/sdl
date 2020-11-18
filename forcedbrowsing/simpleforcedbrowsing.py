from flask import Flask, render_template, request, make_response
import sqlite3
import random

app = Flask(__name__)

@app.route('/users/<user>/secrets')
def handle(user):
    return "here are your secrets, {}: CREDIT CARD: 5243-3213-5455-{} cvv: 777".format(user, user)
