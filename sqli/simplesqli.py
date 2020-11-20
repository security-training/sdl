from flask import Flask, render_template, request, make_response
import sqlite3
import random

try:
    conn=sqlite3.connect('users.db')
    conn.execute("create table users(username text, cookie text);")
    conn.commit
except Exception as e:
    print(e)

app = Flask(__name__)

@app.route('/users/create/<user>')
def createuser(user):
    try:
        cookie=str(random.randint(1000, 9999))
        response=make_response("hello {}".format(user))
        response.set_cookie('cookie', cookie)
        conn=sqlite3.connect('users.db')
        q="insert into users (username, cookie) values ('{}', '{}');".format(user, cookie)
        conn.execute(q)
        conn.commit()
        return response
    except Exception as e:
        print(e)


@app.route('/users/<user>')
def handle(user):
    try:
        conn=sqlite3.connect('users.db')
        q="select cookie from users where username='{}' and cookie='{}';".format(user, request.cookies.get('cookie'))
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if rows==[]:
            return "no cookie error for query: {}".format(q)
        else:
            print(q)
            return "here are your cookies, {} {}".format(user, str(rows))
    except Exception as e:
        print(e)
