from flask import Flask, render_template, request, make_response, redirect
import urllib
import pdb
import string
import random

f=open('keys.txt', 'w')
for i in range(1000):
    key = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    print(key)
    f.write(key+'\r\n')
