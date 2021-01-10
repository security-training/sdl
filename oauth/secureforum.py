from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random
import jinja2
import json
import os
from oauthlib.oauth2 import WebApplicationClient
import requests

try:
    conn=sqlite3.connect('users.db')
    conn.execute("create table users(username text, cookie text, message text);")
    conn.commit
except Exception as e:
    print(str(e))

app = Flask(__name__)

# based on https://realpython.com/flask-google-login/
GOOGLE_CLIENT_ID = "619014629195-1ghgoqecllpvtioa0ks73oc4giqv3p8a.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "IJcRldmBvDtjob8e7oJF84ku"
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL, verify = False).json()

@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = client.prepare_token_request(
    token_endpoint,
    authorization_response=request.url,
    redirect_url=request.base_url,
    code=code
    )
    token_response = requests.post(
    token_url,
    headers=headers,
    data=body,
    auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    verify = False)
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body, verify = False)
    print(userinfo_response)
    cookie=str(random.randint(1000, 9999))
    response=make_response(redirect("/"))
    response.set_cookie('cookie', cookie, httponly=True)
    createuser(userinfo_response.json()["email"], cookie)
    return response


@app.route('/login')
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

def postmessage(user, message):
    try:
        #tm = jinja2.Template('{{message|e}}')
        #message=tm.render(message=message)
        print(message)
        conn=sqlite3.connect('users.db')
        q="insert into users (username, message) values ('{}', '{}');".format(user, message)
        conn.execute(q)
        conn.commit()
        return True
    except Exception as e:
        return str(e)

def createuser(user, cookie):
    try:
        conn=sqlite3.connect('users.db')
        q="insert into users (username, cookie) values ('{}', '{}');".format(user, cookie)
        conn.execute(q)
        conn.commit()
    except Exception as e:
        return str(e)

def verifyuser(user, cookie):
    conn=sqlite3.connect('users.db')
    q="select username, cookie from users where username='{}' and cookie='{}'".format(user,cookie)
    cur = conn.cursor()
    cur.execute(q)
    rows = cur.fetchall();
    conn.commit()
    if rows==[]:
        return False
    else:
        return True

def getuser(cookie):
    conn=sqlite3.connect('users.db')
    q="select username from users where cookie='{}'".format(cookie)
    cur = conn.cursor()
    cur.execute(q)
    rows = cur.fetchall();
    conn.commit()
    if rows==[]:
        return "cheater"
    else:
        return rows[0][0]

@app.route('/post')
def rxss():
    name=request.args.get("name")
    message=request.args.get("message")
    response=make_response(redirect("/"))
    cookie=request.cookies.get('cookie')
    if verifyuser(name, cookie):
        postmessage(name, message)
    else:
        return "cheater!"
    return response


@app.route('/', methods=['POST'])
def add():
    try:
        name=request.form["name"]
        message=request.form["message"]
        response=make_response(redirect("/"))
        if request.cookies.get('cookie')==None:
            return redirect('/')
        else:
            cookie=request.cookies.get('cookie')
            if verifyuser(name, cookie):
                postmessage(name, message)
            else:
                return "cheater!"
        return response
    except Exception as e:
        return "error: make sure you enter name and message "+str(e)

@app.route('/')
def users():
    try:
        conn=sqlite3.connect('users.db')
        q="select username, message from users where message != ''"
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if request.cookies.get('cookie')==None:
            return redirect('/login')
        else:
            user=getuser(request.cookies.get('cookie'))
        form="<h2><form action='/' method='post'>Your Name <input name='name' value={}><p>Message <input name='message' value='' autofocus><p><input type='submit' value='Post Message' style='background-color:lightgreen'></form>".format(user)
        table="<style>td {text-align: left;} .green {text-shadow: 2px 2px 5px green;}</style><h1 class='green'>Friends Forum</h1><hr class='green'><table>"
        for r in rows:
            table+="<tr><td class='green'>from {}</td><td>{}</td></tr>".format(r[0], r[1])
        response=make_response("{}</table>{}".format(table, form))
        return response
    except Exception as e:
        return str(e)
