from flask import Flask, render_template, request, make_response, redirect, send_file
import sqlite3
import random
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

app = Flask(__name__)

users = {
    "יוני": generate_password_hash("bryce"),
    "moshe": generate_password_hash("moshe123")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    return False

@app.route('/')
@auth.login_required
def login():
    cookie=str(random.randint(1000, 9999))
    response=make_response(redirect("/users/{}/public".format(auth.current_user())))
    response.set_cookie('{}-cookie'.format(auth.current_user()), cookie)
    global users
    users.update({'{}-cookie'.format(auth.current_user()):cookie})
    return response


@app.route('/users/<user>/public')
def public(user):
    lines=open('songs.txt','r',encoding='utf-8').readlines()
    line=""
    r=random.randint(1000, 9999)
    while line.rfind('.')==-1:
        line+=lines[r]
        r+=1
    return "<body bgcolor=rgb({},{},{}) dir='rtl'><h1><font color='white'> הפרופיל של {} <img src=../{}/internal/profile.png><p><h3> {} ".format(random.randint(0, 255),random.randint(0, 255),random.randint(0, 255),user,user,line)

@app.route('/users/<user>/internal')
@auth.login_required
def internal(user):
    cookie=request.cookies.get('{}-cookie'.format(user))
    if (cookie!=None) and users.get(user+'-cookie')==cookie:
        return "<body bgcolor=red dir='rtl'><b><code>מידע סודי לעיניך בלבד {}<br>----------------------------------------------<p>פרטי כרטיס אשראי {}:<p> {}-3213-5455-{} cvv: 777".format(user, user, str(random.randint(1000, 9999)),str(random.randint(1000, 9999)) )
    else:
        return "problem with cookie, please log in"

@app.route('/users/<user>/internal/profile.png')
@auth.login_required
def pic(user):
    return send_file('users/internal/profile.png')
