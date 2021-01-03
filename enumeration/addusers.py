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
        q="select username, cookie from users where username='{}';".format(user)
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if rows==[]:
            print(q)
            return "add some users first".format(q)
        else:
            r=""
            for i in rows:
                r+="{} has {} shekel in the bank\r\n".format(i[0], i[1])
            return r
    except Exception as e:
        return str(e)+'. SQL query is '+q
