# https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/

from flask import Flask, render_template, request, make_response, render_template_string
import html
import urllib
import time
import re

app = Flask(__name__)

@app.route("/ssti/<username>")
def ssti(username):
    decoded="Hello, "+urllib.parse.unquote(username)+", today is {{time.ctime()}}"
    t= render_template_string(decoded, time=time)
    return t

@app.route("/nossti/<username>") # filter
def nossti(username):
    for i in re.findall("[{}]", username):
        username=username.strip(i)
    decoded="Hello, "+urllib.parse.unquote(username)+", today is {{time.ctime()}}"
    t= render_template_string(decoded, time=time)
    return t

@app.route("/ssti/", methods=['POST'])
def sstipost():
    username=request.form.get("username")
    print(username)
    decoded="Hello, "+urllib.parse.unquote(username)+", today is {{time.ctime()}}"
    print(decoded)
    t= render_template_string(decoded, time=time)
    return t

@app.route("/")
def menu():
    return """
    <body><h2>
    <a href='/ssti/your-name'>Where is SSTI?</a>
    </body>
    """
