import hashlib
from flask import Flask, render_template, request, make_response, redirect
import urllib

app = Flask(__name__)

grade="78"
gradehash=hashlib.sha1()
gradehash.update(bytes(grade, 'utf-8'))
print("grade hash is {}".format(gradehash.hexdigest()))

html = """
<html><body>
<h1>Grades
<form><p>
Name:<input name='name' id='grade'><p>
Grade:<textarea readonly name='grade' id='grade'>
{}
</textarea>
<input type=submit>
</form>
</body></html>
""".format(grade)

def validate(input):
    print(grade)
    print(input)
    inputhash=hashlib.sha1()
    inputhash.update(input)
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
    if request.args.get('grade')!=None:
        input= request.args.get('grade')
        decodedgrade=urllib.parse.unquote(input).strip()
        if validate(bytes(decodedgrade, 'utf-8')):
            return html
        else:
            return "cheater!"
    else:
        return html
