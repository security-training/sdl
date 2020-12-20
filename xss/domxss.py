from flask import Flask, render_template, request
import urllib.parse
import random

app = Flask(__name__)

@app.route("/calc")
def calc():
    return "Input a number: <input id='num' onchange=c()><div id='area'></div><script>function c() { q=document.getElementById('num').value; if (Number.isNaN(parseInt(q)) || typeof(parseInt(q))!='number') { document.getElementById('area').innerHTML=unescape(q)+' is not a number';} else {document.getElementById('area').innerHTML=unescape(q)+' is a number';} document.getElementById('num').value='';}</script>"
    #return "<body><script>document.body.innerHTML=eval({})</script></body>".format(urllib.parse.unquote(request.args.get('e')))
