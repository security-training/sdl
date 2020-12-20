from flask import Flask, render_template, request, make_response, redirect
from flask_httpauth import HTTPBasicAuth
from random import randint
import os

app = Flask(__name__)

#import sdlutils.auth

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

csrf_token=""

def secure_form(csrf_token):
    html = """
    <html><body>
    <h1>Transfer Money<img src=https://www.flaticon.com/svg/static/icons/svg/3716/3716811.svg>
    <form method='post' action='transfer'><p>
    Amount:<input name='amount'><p>
    To:<input name='to'>
    <input type='hidden' name='csrf_token' value='{}'/>
    <input type=submit>
    </form>
    </body></html>
    """.format(csrf_token)
    return html

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


@auth.login_required
@app.route('/transfer', methods=['GET'])
def anti_csrf():
    global csrf_token
    csrf_token=os.urandom(32).hex()
    return secure_form(csrf_token)

@auth.login_required
@app.route('/transfer', methods=['POST'])
def transfer():
    try:
        user_csrf_token=request.form["csrf_token"]
    except:
        return "bad token"
    global csrf_token
    print("token from request: "+user_csrf_token)
    print("token from memory: "  +csrf_token)
    if user_csrf_token==csrf_token:
        dest=request.form["to"]
        return "money transferred to {}".format(dest)
    else:
        return "unauthorized"
