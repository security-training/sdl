from flask import Flask, render_template, request, make_response, redirect
from flask_httpauth import HTTPBasicAuth
import sdlutils.sdlauth as myauth
import os

app = Flask(__name__)

#import sdlutils.auth

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if (myauth.verify_password(username, password)):
        return True

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

@app.route('/login')
@auth.login_required
def mylogin():
    response=make_response(redirect("/transfer"))
    return myauth.login(response)

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
    print(user_csrf_token)
    print(csrf_token)
    if user_csrf_token==csrf_token:
        dest=request.form["to"]
        return "money transferred to {}".format(dest)
    else:
        return "unauthorized"
