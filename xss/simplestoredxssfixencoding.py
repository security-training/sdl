from flask import Flask, render_template, request, make_response
import sqlite3
import random
import jinja2

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
        tu = jinja2.Template('{{user|e}}')
        encodeduser=tu.render(user=user)
        response=make_response("hello {}".format(encodeduser))
        response.set_cookie('cookie', cookie)
        conn=sqlite3.connect('users.db')
        tc = jinja2.Template('{{cookie|e}}')
        encodedcookie=tc.render(cookie=cookie)
        q="insert into users (username, cookie) values ('{}', '{}');".format(encodeduser, encodedcookie)
        conn.execute(q)
        conn.commit()
        return response
    except Exception as e:
        print(e)


@app.route('/users')
def handle():
    try:
        conn=sqlite3.connect('users.db')
        q="select * from users"
        cur = conn.cursor()
        cur.execute(q)
        rows = cur.fetchall();
        conn.commit()
        if rows==[]:
            return "no users"
        else:
            tr=jinja2.Template('{{rows|e}}')
            encodedrows=tr.render(rows=rows)
            return str(rows)
    except Exception as e:
        print(e)
