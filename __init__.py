from lxml import html
from bs4 import BeautifulSoup
import requests
from flask import Flask,render_template
app=Flask(__name__)

@app.route('/')
def index():
    page = requests.get("http://www.espn.com/tennis/schedule")
    soup = BeautifulSoup(page.content,'html.parser')
    soup.prettify()
    current = []
    upcoming = []
    completed = []
    tables = soup.find_all("table")
    for tr in tables[0].find_all("tr")[2:]:
        tds = tr.find_all("td")
        print("Date: %s, Name: %s, Location: %s"%(tds[0].text, tds[1].text, tds[2].text))


    return render_template("index.html")





 






if __name__=="__main__":
    app.run()
