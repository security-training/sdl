from flask import Flask, render_template, request
import urllib.parse
import random

app = Flask(__name__)

@app.route("/")
def d():
    return "<h1>Enter a number in the URL, for example: http://localhost:5000/5"

@app.route("/<q>")
def calc(q):
    html = """
    <style>td {{text-align: left;}} .green {{text-shadow: 2px 2px 5px green;}}</style>
    <h1 class='green'>Magic Numbers</h1>
    <div id='area'></div>
    <img src='static/xss.jpg'>
    <script>
    q='{}';
    if (!Number.isNaN(parseInt(q)) && typeof(parseInt(q))=='number' && q.match(/[^0-9]/g)==null)
    {{
        document.getElementById('area').innerHTML=unescape(q)+' is a number';
    }}
    else
    {{
        document.getElementById('area').innerHTML=unescape(q)+' is not a number';
    }}
    </script>
    """
    return html.format(q)
    #return "<body><script>document.body.innerHTML=eval({})</script></body>".format(urllib.parse.unquote(request.args.get('e')))
