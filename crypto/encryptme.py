import hashlib
from flask import Flask, render_template, request, make_response, redirect
import urllib
import json
from json import JSONEncoder
from base64 import b64encode
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import pdb

app = Flask(__name__)

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

def cryptme(data):
    print(key)
    ct_bytes = cipher.encrypt(pad(bytes(data, 'utf-8'), AES.block_size))
    return ct_bytes.hex()

html = """
<html><body>
<h1>Encrypt Me!</h1>
<form><p>
Text to encrypt:<input name='data' id='data' value='{}'><p>
<input type=submit value='encrypt!'><p>
Encrypted Text:<p><textarea cols='50' rows='10' readonly name='ct' id='ct'>
{}
</textarea>
</form>
</body></html>
"""

@app.route('/')
def r():
    if request.args.get('data')!=None:
        data= request.args.get('data')
        return html.format(data, cryptme(data))
    else:
        return html.format('','')
