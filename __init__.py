from lxml import html
from bs4 import BeautifulSoup
import requests
import ast
from flask import Flask,render_template
from flask_socketio import SocketIO
from pywebpush import webpush

app=Flask(__name__,static_url_path='')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("try.html")

@socketio.on('subscription_id')
def socfunc(json):
    print("event received")
    print(json)
    print(type(json))
    if json!="":
            y = ast.literal_eval(json)
            print(y)
            webpush(y,
                    data="hello",
                    vapid_private_key="BJhrKdfEX8iXbMrgnHA8vgBwcKCQ4zhYii-g2pGt_LqrDufvux9NIORwP_WHec119BxflFDUEBxVJBv6AZSPmKY",
                    vapid_claims={"sub": "mailto:icm2015003@iiita.ac.in"})


   
    


@app.route('/schedule')
def schedule():
    page = requests.get("http://www.espn.com/tennis/schedule")
    soup = BeautifulSoup(page.content,'html.parser')
    soup.prettify()
    tables = soup.find_all("table")
    return render_template("")
    for tr in tables[0].find_all("tr")[2:]:
        tds = tr.find_all("td")
        print("Date: %s, Name: %s, Location: %s"%(tds[0].text, tds[1].text, tds[2].text))


    return render_template("index.html")



if __name__=="__main__":
    socketio.run(app)

