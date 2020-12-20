import requests
from lxml import html

token=""

file=open("tokens", 'w')

def start_token():
    global token
    while(True):
        page=requests.get("http://localhost:60782/Account/Manage")
        tree = html.fromstring(page.content)
        token=page.headers["Set-Cookie"].split(';')[0].split('=')[1]
        print("got token {}".format(token))
        file.write(token+'\r\n')

def main():
    start_token()

if __name__=="__main__":
    main()
