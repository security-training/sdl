from flask_httpauth import HTTPBasicAuth
from flask import Flask, render_template, request, make_response, redirect
import sys
import os
sys.path.append(os.getcwd())
import sdlutils.sdlauth as myauth

app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if (myauth.verify_password(username, password)):
        return True

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
    response=make_response(redirect("/"))
    return response


@app.route('/login')
@auth.login_required
def mylogin():
    response=make_response(redirect("/transfer"))
    return myauth.login(response)

@auth.login_required
@app.route('/transfer', methods=['GET'])
def csrf():
    return html

@auth.login_required
@app.route('/transfer', methods=['POST'])
def process():
    dest=request.form["to"]
    return "money transferred to {}".format(dest)
