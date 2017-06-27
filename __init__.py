from lxml import html
from bs4 import BeautifulSoup
import requests
import ast
from flask import Flask,render_template
from flask_socketio import SocketIO
from pywebpush import webpush
#from solidwebpush import Pusher

app=Flask(__name__,static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#pusher = Pusher()
#print(pusher.getUrlB64PublicKey())


@app.route('/')
def index():
    return render_template("try.html")

@app.route('/players')
def players():
    return render_template("try.html")

@app.route('/index')
def ind():
    return render_template("index.html")

@app.route('/notification')
def fn():
    print(y)
    

@socketio.on('subscription_id')
def socfunc(json):
    print("event received")
    print(json)
    print(type(json))
    if json!="":
        #pusher.sendNotification(json, "Hello World")
            global y 
            y = ast.literal_eval(json)
            print(y)
            webpush(y,
                    data="hello",
                    vapid_private_key="tgX_vQz113iCfMtdEW41oaLQFyKb3fjP4x4nkDw0AMs",
                    vapid_claims={"sub": "mailto:icm2015003@iiita.ac.in","aud":"https://fcm.googleapis.com"})


   
    


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
        index+=1
    print(curretable)    

    return render_template('schedule.html',tables=curretable)



if __name__=="__main__":
    socketio.run(app)

