from lxml import html
from bs4 import BeautifulSoup
from datetime import datetime
import requests

import ast
import threading
from flask import Flask,render_template
from flask_socketio import SocketIO
from pywebpush import webpush
#from solidwebpush import Pusher

y=[]

def notif():
    print("working")
    hours = datetime.now().strftime("%H")
    print(hours)
    minutes = datetime.now().strftime("%M")
    seconds = datetime.now().strftime("%S")
    page = requests.get("http://www.espn.com/tennis/schedule")
    soup = BeautifulSoup(page.content,'html.parser')
    soup.prettify()
    tables = soup.find_all("table")
    currtable = tables[0].find_all("tr")[2:]
    curretable=[]
    for tr in tables[0].find_all("tr")[2:]:
        tds = tr.find_all("td")
        curretable.append(tds[1].text)

    print(curretable)
    if hours == "00":
        print("time to send a notification")
        if y:
            print(y[0])
            m = ast.literal_eval(y[0]['endpoint'])
            print(m)
            webpush(m,
                    data=str(curretable),
                    vapid_private_key="tgX_vQz113iCfMtdEW41oaLQFyKb3fjP4x4nkDw0AMs",
                    vapid_claims={"sub": "mailto:icm2015003@iiita.ac.in","aud":"https://fcm.googleapis.com"})


    
    
    
app=Flask(__name__,static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
#pusher = Pusher()
#print(pusher.getUrlB64PublicKey())

set_interval(notif,15)


@app.route('/')
def index():
    return render_template("try.html")

    

@socketio.on('subscription_id')
def socfunc(json):
    print("event received")
    print(json)
    print(type(json))
    if json!="":
        #pusher.sendNotification(json, "Hello World")
            global y 
            #y = ast.literal_eval(json.endpoint)
            y.append(json)
            print(y)
            #webpush(y,
             #       data="hello",
              #      vapid_private_key="tgX_vQz113iCfMtdEW41oaLQFyKb3fjP4x4nkDw0AMs",
               #     vapid_claims={"sub": "mailto:icm2015003@iiita.ac.in","aud":"https://fcm.googleapis.com"})


   
    


@app.route('/schedule')
def schedule():
    print("inside schedule")
    page = requests.get("http://www.espn.com/tennis/schedule")
    soup = BeautifulSoup(page.content,'html.parser')
    soup.prettify()
    tables = soup.find_all("table")
    currtable = tables[0].find_all("tr")[2:]
    curretable = [[],[],[]]
    index = 0
    for tr in tables[0].find_all("tr")[2:]:
        tds = tr.find_all("td")
        curretable[index].append(tds[0].text)
        curretable[index].append(tds[1].text)
        curretable[index].append(tds[2].text)
        curretable[index].append(tds[1].a['href'])
        index+=1
    print(curretable) 

    arr= tables[2].find_all("tr")[2:]
    l = len(arr)
    curretable2=[[] for i in range(l)]
    print(curretable2)
    print(l)
    inde=0
    for tr in tables[2].find_all("tr")[2:]: 
            tds = tr.find_all("td")
            curretable2[inde].append(tds[0].text)
            curretable2[inde].append(tds[1].text)
            curretable2[inde].append(tds[2].text)
            curretable2[inde].append(tds[1].a['href'])
            inde+=1
    print(curretable2)


    return render_template('schedule.html',tables=curretable,tables2=curretable2)

@app.route('/rankings')
def rankings():
    page = requests.get("http://www.espn.com/tennis/rankings")
    soup = BeautifulSoup(page.content,'html.parser')
    soup.prettify()
    tables = soup.find_all("table")
    arr= tables[0].find_all("tr")[2:]
    l = len(arr)
    curretable3=[[] for i in range(l)]
    #print(curretable3)
    #print(l)
    index2=0
    for tr in tables[0].find_all("tr")[2:]: 
            tds = tr.find_all("td")
            print(tds[3].find_all('div'))
            curretable3[index2].append(tds[0].text)
            curretable3[index2].append(tds[1].text)
            curretable3[index2].append(tds[2].img['src'])
            curretable3[index2].append(tds[3].find_all('div')[1].text)
            curretable3[index2].append(tds[4].text)
            curretable3[index2].append(tds[1].a['href'])
            curretable3[index2].append(tds[3].find_all('div')[0].img['src'])
            index2+=1
    print(curretable3)
    return render_template('rankings.html',tables3=curretable3)

    


if __name__=="__main__":
    socketio.run(app)

