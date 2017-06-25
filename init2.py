from bs4 import BeautifulSoup
import requests
a = requests.get("http://games.espn.com/fba/scoreboard?leagueId=224165&seasonId=2017")
soup = BeautifulSoup(a.text, 'lxml')
# searching for the rows directly
rows = soup.findAll('tr', {'class': 'linescoreTeamRow'})
# you will need to isolate elements in the row for the table
for row in rows:
    print(row.text)