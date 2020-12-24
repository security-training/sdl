from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random

auth = HTTPBasicAuth()

try:
    conn=sqlite3.connect('users.db')
    conn.execute("create table users(username text, cookie text);")
    conn.commit
except Exception as e:
    print(e)

app = Flask(__name__)

users = {
    "admin": generate_password_hash("secret")
}

@auth.verify_password
def verify_password(username, password):
    conn=sqlite3.connect('users.db')
    q="select distinct username, cookie from users where username='{}' and cookie='{}';".format(username, password)
    cur = conn.cursor()
    cur.execute(q)
    rows = cur.fetchall();
    conn.commit()
    if rows==[]:
        return False
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    return False

@app.route('/')
@auth.login_required
def login():
    html="""
    <body bgcolor='lightgray'>
    <h1>SQL Bank Admin Panel</h1><p>
    <form action='/users/create' method='POST'>
    Add User:<input autofocus name='user'><p>
    Add Balance:<input name='balance'><p>
    <input type='submit'>
    </form>
    """
    return html


@app.route('/users/create', methods=['POST'])
@auth.login_required
def createuser():
    try:
        user=request.form["user"]
        balance=request.form["balance"]
        conn=sqlite3.connect('users.db')
        q="insert into users (username, cookie) values ('{}', '{}');".format(user, balance)
        conn.execute(q)
        conn.commit()
        response=make_response(redirect("/users/"+user))
        return response
    except Exception as e:
        print(e)


@app.route('/users/<user>')
@auth.login_required
def handle(user):
    try:
        conn=sqlite3.connect('users.db')
        q="select distinct username, cookie from users where username='{}';".format(user)
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if rows==[]:
            return "user does not exist".format(q)
        else:
            table="<table>"
            for r in rows:
                table+="<tr><td class='green'>Added user {}</td><td>balance {}</td></tr>".format(r[0], r[1])
            response=make_response("{}</table>".format(table))
            return response
    except Exception as e:
        return str(e)+'. SQL query is '+q
