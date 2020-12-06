from flask_httpauth import HTTPBasicAuth
from flask import Flask, render_template, request, make_response, redirect
from random import randint

app = Flask(__name__)

auth = HTTPBasicAuth()

users = {
    "john": "bryce"
}

@auth.verify_password
def verify_password(username, password):
    if (username, password) == ('', ''):
        return False
    if users[username]==password:
        return True
    return False

html = b"""
<html><body>
<h1>Transfer Money<img src=https://www.flaticon.com/svg/static/icons/svg/3716/3716811.svg>
<form method='post' action='transfer'><p>
Amount:<input name='amount'><p>
To:<input name='to'>
<input type=submit>
</form>
</body></html>
"""

@app.route('/')
@auth.login_required
def r():
    response=make_response(redirect("/login"))
    return response

@app.route('/login')
@auth.login_required
def login():
    response=make_response(redirect("/transfer"))
    cookie=str(randint(1000, 9999))
    response.set_cookie('cookie', cookie)
    return response

@app.route('/transfer', methods=['GET'])
@auth.login_required
def csrf():
    return html

@app.route('/transfer', methods=['POST'])
@auth.login_required
def process():
    dest=request.form["to"]
    return "money transferred to {}".format(dest)
