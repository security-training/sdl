from flask import Flask, render_template
from flask_basicauth import BasicAuth

class MyAuth(BasicAuth):
    def check_credentials(self, username, password):
        if username!=app.config['BASIC_AUTH_USERNAME']:
            return 'bad username'
        if password!=app.config['BASIC_AUTH_PASSWORD']:
            return 'bad password'


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'john'
app.config['BASIC_AUTH_PASSWORD'] = 'matrix'


basic_auth = MyAuth(app)

@app.route('/secret')
@basic_auth.required
def secret_view():
    return render_template('secret.html')
