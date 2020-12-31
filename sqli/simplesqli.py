from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random
import pdb

Session={'cookie':''}

try:
    conn=sqlite3.connect('users.db')
    conn.execute("create table users(username text, password text);")
    conn.commit()
except Exception as e:
    conn.execute("insert into users (username, password) values ('admin', 'secret');")
    conn.commit()
    print(e)

app = Flask(__name__)

@app.route('/authenticate', methods=['POST'])
def verify_password():
    try:
        username=request.form["username"]
        password=request.form["password"]
        conn=sqlite3.connect('users.db')
        q="select  username, password from users where username='{}' and password='{}';".format(username, password)
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        print(q)
        if rows==[]:
            return "bad username or password"
    except Exception as e:
        return str(e)+" "+q
    cookie=str(random.randint(1000, 9999))
    Session['cookie']=cookie
    response=make_response(redirect("/panel"))
    response.set_cookie('sqli-cookie', cookie)
    return response

@app.route('/')
def login():
    html="""
    <body bgcolor='black'><font color='lightgreen'>
    <h1>SQL Bank Admin Login</h1><p>
    <form action='/authenticate' method='POST'>
    Username:<input autofocus name='username'><p>
    Password:<input type=password name='password'><p>
    <input type='submit'>
    </form>
    """
    return html

@app.route('/panel')
def panel():
    if request.cookies.get('cookie')!=Session['cookie']:
        response=make_response(redirect("/"))
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
def createuser():
    if request.cookies.get('cookie')!=Session['cookie']:
        response=make_response(redirect("/"))
    try:
        user=request.form["user"]
        balance=request.form["balance"]
        conn=sqlite3.connect('users.db')
        q="insert into users (username, password) values ('{}', '{}');".format(user, balance)
        conn.execute(q)
        conn.commit()
        response=make_response(redirect("/users/"+user))
        return response
    except Exception as e:
        return str(e)+" "+q


@app.route('/users/<user>')
def handle(user):
    if request.cookies.get('cookie')!=Session['cookie']:
        response=make_response(redirect("/"))
    try:
        conn=sqlite3.connect('users.db')
        q="select distinct username, password from users where username='{}';".format(user)
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
