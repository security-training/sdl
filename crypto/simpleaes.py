import hashlib
from flask import Flask, render_template, request, make_response, redirect
import urllib
import json
from json import JSONEncoder
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

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

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(bytes(json_data, 'utf-8'), AES.block_size))
iv = b64encode(cipher.iv).decode('utf-8')
ct = b64encode(ct_bytes).decode('utf-8')
crypt_json = json.dumps({'iv':iv, 'ciphertext':ct})

gradehash=hashlib.sha1()
gradehash.update(bytes(ct, 'utf-8'))
print("grade hash is {}".format(gradehash.hexdigest()))

html = """
<html><body>
<h1>Grades
<form><p>
Name:<input name='name' id='grade'><p>
Grade:<textarea readonly name='grade' id='grade'>
{}
</textarea>
<input type=hidden name='state' value='{}'>
<input type=submit>
</form>
</body></html>
""".format(g.grade, ct)

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
    if request.args.get('state')!=None:
        input= request.args.get('state')
        decodedjson=urllib.parse.unquote(input).strip()
        if validate(bytes(decodedjson, 'utf-8')):
            return html
        else:
            return "cheater!"
    else:
        return html
