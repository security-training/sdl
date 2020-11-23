from flask import Flask, render_template, request
import urllib.parse
import random

app = Flask(__name__)

@app.route("/calc")
def calc():
    #return "<script>q=document.location.search.split('?')[1].split('=')[1]; if (typeof(q)!=BigInt) { document.write(unescape(q)+' is not a number')}</script>"
    return "<body><script>document.body.innerHTML=eval({})</script></body>".format(urllib.parse.unquote(request.args.get('e')))
