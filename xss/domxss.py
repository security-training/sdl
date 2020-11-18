from flask import Flask, render_template, request
import urllib.parse
import random

app = Flask(__name__)

@app.route("/calc")
def calc():
    return "<body><script>document.body.innerHTML=eval({})</script></body>".format(urllib.parse.unquote(request.args.get('e')))
