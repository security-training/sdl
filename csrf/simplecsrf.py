from flask_httpauth import HTTPBasicAuth
from flask import Flask, render_template, request, make_response, redirect
import sys
import sdlutils.auth as myauth

app = Flask(__name__)

import sdlutils.auth

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

@app.route('/login')
@auth.login_required
def mylogin():
    return myauth.login("/transfer")

@auth.login_required
@app.route('/transfer', methods=['GET'])
def csrf():
    return html

@auth.login_required
@app.route('/transfer', methods=['POST'])
def process():
    dest=request.form["to"]
    return "money transferred to {}".format(dest)


#https://github.com/payloadbox/xxe-injection-payload-list
