import requests

f=open('users.txt','r')
for user in f.readlines():
	r=requests.get('http://localhost:5000/users/create/{}'.format(user.strip()))
	print(r.text)
