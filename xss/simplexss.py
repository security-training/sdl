from flask import Flask, render_template, request
import urllib.parse
import random

def page_not_found(e):
    response=e.get_response()
    #response.content_type="application/json"
    if request.cookies.get('cookie')==None:
        cookie=str(random.randint(1000, 9999))
        response.set_cookie('cookie', cookie, httponly=True)
    else:
        cookie=request.cookies.get('cookie')
    response.data='the {} does not exist'.format(urllib.parse.unquote(request.url))
    return response, 404

app = Flask(__name__)
app.register_error_handler(404, page_not_found)
