#https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

#openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

#flask run --cert=cert.pem --key=key.pem

import os

print(os.getpid())
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Crypto World!"

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
