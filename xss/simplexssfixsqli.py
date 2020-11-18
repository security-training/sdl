from flask import Flask, render_template, request
import urllib.parse
import sqlite3
import random

try:
    conn.execute("create table urls(url text, cookie text)")
except:
    pass


# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
def page_not_found(e):
    conn=sqlite3.connect('urls.db')
    response=e.get_response()
    response.content_type="application/json"
    response.data='the {} does not exist: '.format(urllib.parse.unquote(request.url))
    if request.cookies.get('cookie')==None:
        cookie=str(random.randint(1000, 9999))
        response.set_cookie('cookie', cookie)
    else:
        cookie=request.cookies.get('cookie')
    q1="insert into urls (url, cookie) values ('{}', '{}');".format(cookie,urllib.parse.unquote(request.path.strip('/')))
    print(q1)
    try:
        conn.execute(q1)
        conn.commit()
    except Exception as e:
        print(e)
    q2="select url from urls where cookie='{}';".format(cookie)
    print(q2)
    try:
        cur = conn.cursor()
        cur.execute(q2)
        rows = cur.fetchall();
        conn.commit()
        for i in rows:
            c=tuple(i)
            response.data+=bytes(" {}".format(c[0]), 'utf-8')
    except Exception as e:
        print(e)
    conn.close()
    return response, 404

app = Flask(__name__)
app.register_error_handler(404, page_not_found)
