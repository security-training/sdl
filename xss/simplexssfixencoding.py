from flask import Flask, render_template, request
import urllib.parse
import random
import jinja2
#https://jinja.palletsprojects.com/en/2.11.x/templates/

# https://flask.palletsprojects.com/en/1.1.x/patterns/errorpages/
def page_not_found(e):
    response=e.get_response()
    response.content_type="text/html"
    if request.cookies.get('cookie')==None:
        cookie=str(random.randint(1000, 9999))
        response.set_cookie('cookie', cookie)
    else:
        cookie=request.cookies.get('cookie')
    data='the {} does not exist '.format(urllib.parse.unquote(request.url))
    cleandata=data.replace("<script>",'')
    template = jinja2.Template('Error: {{error|e}}')
    return template.render(error=cleandata), 404

app = Flask(__name__)
app.register_error_handler(404, page_not_found)
