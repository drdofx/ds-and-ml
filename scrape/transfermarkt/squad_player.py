import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

club_data = []

url = "https://www.transfermarkt.com/fc-arsenal/startseite/verein/11"    

print(url)

test = requests.get(url, headers=headers)
pageSoup = BeautifulSoup(test.content, 'html.parser')
values = pageSoup.find_all('tr', {"class": ['odd', 'even']})

for i in range(0, len(values)):
    number = values[i].find('td', {'class': "zentriert"}).text
    
    name = values[i].find('div', {'class': 'di nowrap'}).text
    
    # position = values[i].find('td', {'class': 'zentriert'})['title']
    position = values[i].find('table', {'class': 'inline-table'}).findAll("tr")[1].text
    print(position)
    
    nationality = values[i].find('img', {'class': 'flaggenrahmen'})['title']

    market_val = values[i].find('td', {'class': 'rechts hauptlink'}).text
    market_val = market_val.replace(u'\xa0', '')

    data = {
        "squadNumber": number,
        "name": name,
        "position": position,
        "nationality": nationality,
        "marketValue": market_val
    }   

    club_data.append(data)


print(club_data)
with open('arsenal2122.json', 'w') as fout:
    json.dump(club_data, fout)