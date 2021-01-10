from lxml import etree # https://lxml.de/parsing.html
from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

payload = b"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY>
<!ENTITY xxe SYSTEM 'file://users//admin//secrets.txt'>
]>
<foo>
&xxe;
</foo>"""

@app.route('/')
def home():
    return "<h1>XML Checker</h1><p>Enter your XML below:<p><form method=post action='/xml'><textarea name='xml' cols='50' rows='20'></textarea><input type=submit>"

@app.route('/xml', methods=['POST'])
def xml():
    try:
        xml = request.form["xml"].encode()
        print(xml)
        parser = etree.XMLParser(resolve_entities=False)
        doc = etree.fromstring(xml, parser)
        parsed_xml = etree.tostring(doc)
        return parsed_xml
    except Exception as e:
        print(e)
        return "This is bad XML"

#https://github.com/payloadbox/xxe-injection-payload-list
