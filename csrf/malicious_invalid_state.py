from flask import Flask, render_template, request, make_response, redirect
import requests
import time
from lxml import html

app = Flask(__name__)

data="__EVENTTARGET=&__EVENTARGUMENT=&__VIEWSTATE=ZtJcgIgwFRzIrOY%2BsPY4n1TuVGaHQz4VebA9MX4tzWGxH1%2BpEqK%2Bd%2FB66uZE8IwkobogctAvhxOomVWgkMaUdMnfKNOjfJ8epfhcWZR8kU%2FJbKjKmOXUQPiXxjYlaLyKWYHMmZLyhj0dS%2BOBLGeiDe1eCqAk6Niai%2B3dlZ%2F58cgC1a4XUkE6AgjbZNmjA2jl8p%2BiFe%2BLLpVgggANg%2FLPqy4Ztxe%2FSvVM5SwipYrTzBjGHah1MAIvOa8nxFvGe%2F9ZscUfJZ00sbdx3YcJ2QpphB5r3s9unpyrI%2F4XeHEm6t9HRzcJwcU%2BA%2FtPu2s2y3ajDCYiPMVXyVBk2zCfCzv7YhqYAp8%2F0HxnSLAPEBXvsDjrDpfqig8CJJkACuQkmgOv&ctl00%24MainContent%24UserName=tal2&ctl00%24MainContent%24Password=tal2&ctl00%24MainContent%24ctl05=Log+in&__VIEWSTATEGENERATOR=CD85D8D2&__EVENTVALIDATION=%2FJ7pV3kw%2BNVXe%2B%2FIYyU92KiCnymmzMyi%2FqV5tUiCyKwRR0zJ1%2F0MYBG3zJlMAkzImf0ZLFmIrUKQ%2Bqzg%2BBsWon2Ox%2BxNxsd4z9egrQ6ncO%2B0Qksuph5EXmri3K8JzVONb1vXbsesHsDeWBoEPrIYFeyAW%2BwOfgKD8x%2FBzOueHip17%2F7O58wJguCwLMt7OU6q"
@app.route('/', methods=['GET'])
def csrf():
    #page=requests.post("http://localhost:33773/Account/Login", data=data, headers={"Host": "localhost:33773" })
    #print(page.content)
    return render_template("webform.html")
