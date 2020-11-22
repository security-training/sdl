from random import randint

users = {
    "john": "bryce"
}

def verify_password(username, password):
    if users[username]==password:
        return True
    return False

def login(response):
    cookie=str(randint(1000, 9999))
    response.set_cookie('cookie', cookie)
    #response.set_cookie('sdlcookie', cookie, httponly=True, samesite='Strict')
    return response
