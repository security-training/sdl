from flask import Flask, render_template, request, make_response, redirect
import requests
import time
from lxml import html

token=""

def start_token():
    global token
    while(True):
        page=requests.get("http://localhost:33773/Account/Manage")
        tree = html.fromstring(page.content)
        token=page.headers["Set-Cookie"].split(';')[0].split('=')[1]
        print("got token {}".format(token))
        time.sleep(5)

def main():

    start_token()

if __name__=="__main__":
    main()
