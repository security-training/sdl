from flask import Flask, render_template, request, make_response, render_template_string
import requests
import socket

app = Flask(__name__)

html = b"""
<html><body>
Download from S3 Storage
<form action='/'><p>
S3 URL:<input name='url'><p>
<input type='submit'/>
</form>
</body></html>
"""

@app.route("/", methods=["GET"])
def d1():
    if request.args.get("url")==None:
        return html
    else:
        url=request.args.get("url")
        try:
            r=requests.get("{}".format(url), headers={'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwZW50YWdvbiIsImlhdCI6MTYwNzI3Mjc4MCwiZXhwIjoxNjM4ODA4NzgwLCJhdWQiOiJ3d3cucGVudGFnb24ubWlsIiwic3ViIjoiYWRtaW5AcGVudGFnb24ubWlsIiwiYWRtaW4iOiJ0cnVlIiwiU3VybmFtZSI6Ik1hc3RlciIsIkVtYWlsIjoiYWRtaW5AcGVudGFnb24ubWlsIiwiUm9sZSI6WyJNYW5hZ2VyIiwiUHJvamVjdCBBZG1pbmlzdHJhdG9yIl19.7RvPRcCk8Lu-QbQo5vhN82dG6oUMlJyoTRDIErWP9jI'})
            return r.text
        except:
            hostname=socket.gethostname()
            ip=socket.gethostbyname(hostname)
            return "bad request connection refused from interface: eth0: {}/24".format(ip)


@app.route("/download", methods=["POST"])
def d2():
    url=request.form["url"]
    r=requests.get("{}".format(url), headers={'Authentication':'TOPSECRET'})
    return r.text
