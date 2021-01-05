from flask import Flask, render_template, request, make_response, redirect
import urllib.parse
import random

app = Flask(__name__)

@app.route("/<q>")
def d(q):
    if q == None:
        return "<h1>Enter a number in the URL query string, for example: http://localhost:5000/5"
    else:
        response = make_response(redirect("/?q={}".format(q)))
        return response

@app.route("/")
def calc():
    html = """
    <style>td {{text-align: left;}} .green {{text-shadow: 2px 2px 5px green;}}</style>
    <h1 class='green'>Magic Numbers</h1>
    <div id='area'>Enter a number in the URL query string, for example: http://localhost:5000/5</div>
    <img src='static/xss.jpg'>
    <script>
    q=document.location.search.split('?')[1].split('=')[1];
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
    return html.format()
    #return "<body><script>document.body.innerHTML=eval({})</script></body>".format(urllib.parse.unquote(request.args.get('e')))
