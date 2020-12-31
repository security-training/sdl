from flask import Flask, render_template, request
import urllib.parse
import random

app = Flask(__name__)

@app.route("/")
def d():
    return "<h1>Enter a number in the URL, for example: http://localhost:5000/5"

@app.route("/<q>")
def calc(q):
    return "<style>td {text-align: left;} .green {text-shadow: 2px 2px 5px green;}</style><h1 class='green'>Magic Numbers</h1><div id='area'></div><script>q='"+q+"'; if (Number.isNaN(parseInt(q)) || typeof(parseInt(q))!='number') { document.getElementById('area').innerHTML=unescape(q)+' is not a number';} else {document.getElementById('area').innerHTML=unescape(q)+' is a number';} </script>"
    #return "<body><script>document.body.innerHTML=eval({})</script></body>".format(urllib.parse.unquote(request.args.get('e')))
