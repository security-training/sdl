from werkzeug.security import generate_password_hash, check_password_hash
from flask import make_response, redirect
import random

users = {
    "john": generate_password_hash("bryce")
}

def verify_password(username, password):
    if username in users and \
        check_password_hash(users.get(username), password):
        return True
    return False

def login(redirect_url):
    cookie=str(random.randint(1000, 9999))
    response=make_response(redirect(redirect_url))
    response.set_cookie('cookie', cookie)
    return response
