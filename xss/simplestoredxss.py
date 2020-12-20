from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random

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
        createuser(name, message)
        response=make_response(redirect("/"))
        response.set_cookie('cookie', name)
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

@app.route('/')
def users():
    try:
        conn=sqlite3.connect('users.db')
        q="select username, cookie from users"
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if request.cookies.get('cookie')==None:
            user='enter_your_username'
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
