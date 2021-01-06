# https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/

from flask import Flask, render_template, request, make_response, render_template_string
import html
import urllib
import time

app = Flask(__name__)

@app.route("/ssti/<username>")
def ssti(username):
    decoded="Hello, "+urllib.parse.unquote(username)+", today is {{time.ctime()}}"
    t= render_template_string(decoded, time=time)
    return t

@app.route("/ssti/", methods=[POST])
def ssti():
    username=request.form["username"]
    decoded="Hello, "+urllib.parse.unquote(username)+", today is {{time.ctime()}}"
    t= render_template_string(decoded, time=time)
    return t

@app.route("/")
def menu():
    return """
    <body><h2>
    <a href='/ssti/your-name'>Where is SSTI?</a>
    </body>
    """
