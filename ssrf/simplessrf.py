from flask import Flask, render_template, request, make_response, render_template_string
import requests

app = Flask(__name__)

html = b"""
<html><body>
Download from S3 Storage
<form action='/download'><p>
S3 URL:<input name='url'><p>
<input type='submit'/>
</form>
</body></html>
"""

@app.route("/download", methods=["GET"])
def d1():
    if request.args.get("url")==None:
        return html
    else:
        url=request.args.get("url")
        try:
            r=requests.get("{}".format(url), headers={'Authentication':'TOPSECRET'})
            return r.text
        except:
            return "bad request connection refused from interface: eth0: 192.168.1.0/24"


@app.route("/download", methods=["POST"])
def d2():
    url=request.form["url"]
    r=requests.get("{}".format(url), headers={'Authentication':'TOPSECRET'})
    return r.text
