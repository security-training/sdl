from flask import Flask, render_template, request, make_response, redirect
import sqlite3
import random
import jinja2

try:
    conn=sqlite3.connect('users.db')
    conn.execute("create table users(username text, cookie text, message text);")
    conn.commit
except Exception as e:
    print(str(e))

app = Flask(__name__)

def postmessage(user, message):
    try:
        #tm = jinja2.Template('{{message|e}}')
        #message=tm.render(message=message)
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
            cookie=str(random.randint(1000, 9999))
            response.set_cookie('cookie', cookie)
            createuser(name, cookie)
            postmessage(name, message)
            return response
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
            user='enter_your_username'
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
