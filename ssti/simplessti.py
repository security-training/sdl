# https://www.onsecurity.io/blog/server-side-template-injection-with-jinja2/

from flask import Flask, render_template, request, make_response, render_template_string
import jinja2
import urllib

app = Flask(__name__)

@app.route('/nossti/<payload>')
def nossti(payload):
    decoded=urllib.parse.unquote(payload)
    t = jinja2.Template(payload)
    return t.render(payload=decoded)

@app.route("/ssti/<payload>")
def ssti(payload):
    decoded=urllib.parse.unquote(payload)
    return render_template_string(decoded)
