from flask import Flask, render_template, request
import urllib.parse
import random

def page_not_found(e):
    response=e.get_response()
    if request.cookies.get('cookie')==None:
        cookie=str(random.randint(1000, 9999))
        response.set_cookie('cookie', cookie)
    else:
        cookie=request.cookies.get('cookie')
    return '<a onclick=alert("{}")>{}</a> '.format(urllib.parse.unquote(request.url), request.url), 404

app = Flask(__name__)
app.register_error_handler(404, page_not_found)
