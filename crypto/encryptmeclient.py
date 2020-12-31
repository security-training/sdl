from flask import Flask, render_template, request, make_response, redirect
import urllib
import pdb
import string
import random

app = Flask(__name__)

session={"key":""}

@app.route('/decrypt', methods=['POST'])
def decrypt():
    if request.form['ct']!=None:
        ct= request.form['ct']
        data=''
        ctl=ct.split(',')
        key=session["key"]
        i=0
        for c in ctl:
            c=int(c)
            k=ord(key[i])
            dc=c^k
            data+=chr(dc)
            i+=1
        print(data)
        return "your text is: "+data

html = """
<html><body>
<script>
function crypt()
{{
    data=document.getElementById('data').value;
    key=document.getElementById('key').value;
    console.log(key)
    ct=''
    for (i in data)
    {{
        ch=data.charCodeAt(i);
        k=key.charCodeAt(i);
        i==0 ? ct+=parseInt(ch ^ k) : ct+=','+parseInt(ch ^ k);
    }}
    document.getElementById('ct').value=ct;
}}
</script>
<h1>Encrypt Me!</h1>
<form id='frm' action='/decrypt' method='POST'><p>
Text to encrypt:<input id='data' onKeyPress=crypt()><p>
<input type=submit value='decrypt!' onclick=crypt()><p>
<input type='hidden' id='key' value='{}'>
Encrypted Text:<p><textarea cols='50' rows='10' readonly name='ct' id='ct'>
</textarea>
</form>
</body></html>
"""


@app.route('/')
def r():
    key = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    session["key"]=key
    print(session["key"])
    return html.format(key)
