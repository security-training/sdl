import hashlib
from flask import Flask, render_template, request, make_response, redirect
import urllib
import json
from json import JSONEncoder


app = Flask(__name__)

class Grade(dict):
    def __init__(self, grade:str):
        self.grade=grade
        self.year='2020'
        self.school='matrix'
    factor=10
    def factor(self):
        return self.grade;
    def grade(self):
        return self.grade

g=Grade(grade="78")
grade=g.grade
json_data = json.dumps(g.__dict__)

gradehash=hashlib.sha1()
gradehash.update(bytes(json_data, 'utf-8'))
print("grade hash is {}".format(gradehash.hexdigest()))

html = """
<html><body>
<h1>Grades
<form><p>
Name:<input name='name' id='grade'><p>
Grade:<textarea readonly name='grade' id='grade'>
{}
</textarea>
<input type=hidden name='json' value='{}'>
<input type=submit>
</form>
</body></html>
""".format(g.grade, json_data)

def validate(input):
    inputhash=hashlib.sha1()
    inputhash.update(input)
    print("grade hash is {}".format(gradehash.hexdigest()))
    print("input hash is {}".format(inputhash.hexdigest()))
    if inputhash.hexdigest()==gradehash.hexdigest():
        return True
    else:
        return False

@app.route('/')
def r():
    response=make_response(redirect("/grades"))
    return response

@app.route('/grades', methods=['GET'])
def grades():
    if request.args.get('json')!=None:
        input= request.args.get('json')
        decodedjson=urllib.parse.unquote(input).strip()
        if validate(bytes(decodedjson, 'utf-8')):
            return html
        else:
            return "cheater!"
    else:
        return html
