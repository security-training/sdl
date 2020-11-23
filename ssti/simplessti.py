from flask import Flask, render_template, request, make_response, render_template_string
import jinja2

app = Flask(__name__)

@app.route('/nossti/<payload>')
def nossti(payload):
    t = jinja2.Template('{{payload}}')
    return t.render(payload=payload)

@app.route("/ssti/<payload>")
def ssti(payload):
    return render_template_string(payload)
