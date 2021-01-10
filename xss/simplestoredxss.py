from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random
import json
import os
from oauthlib.oauth2 import WebApplicationClient
import requests

try:
    conn=sqlite3.connect('users.db')
    conn.execute("create table users(username text, cookie text);")
    conn.commit
except Exception as e:
    print(str(e))

app = Flask(__name__)

@app.route('/', methods=['POST'])
def add():
    try:
        name=request.form["name"]
        message=request.form["message"]
        response=make_response(redirect("/"))
        if request.cookies.get('cookie')==None:
            response.set_cookie('cookie', name)
            createuser(name, message)
        elif name==request.cookies.get('cookie'):
            name=request.cookies.get('cookie')
            createuser(name, message)
        else:
            return "cheater!"
        return response
    except:
        return "error: make sure you enter name and message"

def createuser(user, message):
    try:
        conn=sqlite3.connect('users.db')
        q="insert into users (username, cookie) values ('{}', '{}');".format(user, message)
        conn.execute(q)
        conn.commit()
        return
    except Exception as e:
        return str(e)

# based on https://realpython.com/flask-google-login/

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")

# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

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
    )
    client.parse_request_body_response(json.dumps(token_response.json()))
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    print(userinfo_response)

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
    try:
        conn=sqlite3.connect('users.db')
        q="select username, cookie from users"
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if request.cookies.get('cookie')==None:
            response=make_response("/login")
            return response
        else:
            user=request.cookies.get('cookie')
        form="<h2><form action='/' method='post'>Your Name <input name='name' value={}><p>Message <input name='message' value='' autofocus><p><input type='submit' value='Post Message' style='background-color:lightgreen'></form>".format(user)
        table="<style>td {text-align: left;} .green {text-shadow: 2px 2px 5px green;}</style><h1 class='green'>Friends Forum</h1><hr class='green'><table>"
        for r in rows:
            table+="<tr><td class='green'>from {}</td><td>{}</td></tr>".format(r[0], r[1])
        response=make_response("{}</table>{}".format(table, form))
        return response
    except Exception as e:
        return str(e)
