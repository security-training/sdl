import requests

def checkuser():
    f=open('users.txt')
    users=f.readlines()
    for user in users:
        try:
            r=requests.get("http://localhost:5000/users/{}".format(user.strip()))
            print("found "+r.text)
        except Exception as e:
            print(e)

checkuser()
