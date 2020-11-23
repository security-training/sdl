from flask import Flask, render_template, request
import urllib.parse
import random

app = Flask(__name__)

@app.route("/calc")
def calc():
    return "<script>q=document.location.search.split('?')[1].split('=')[1]; if (typeof(q)!=BigInt) { document.write(escape(q)+' is not a number')}</script>"
