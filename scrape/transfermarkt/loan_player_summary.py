import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

year = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]

club_data = []

league = "GB1" if int(input("Enter league: ")) == 1 else "L1" # if user input == 1, get EPL data, else get Bundesliga

for y in range(0, len(year)):
    url = f"https://www.transfermarkt.com/premier-league/leihspieler/wettbewerb/{league}/plus/1?saison_id={year[y]}&leihe=ist"    

    print(url)

    test = requests.get(url, headers=headers)
    pageSoup = BeautifulSoup(test.content, 'html.parser')
    values = pageSoup.find_all('tr', {"class": ['odd', 'even']})
    
    for i in range(0, len(values)):
        name = values[i].find('td', {'class': 'hauptlink no-border-links'}).text
        rests = values[i].find_all('td', {'class': 'zentriert'})

        market_val = values[i].find_all('td', {'class': 'rechts'}) 
        
        market_val_end = market_val[1].find('span')['title'] if market_val[1].find('span') else '-'
        
        start_val = market_val[1].text.replace(u'\xa0', '').strip('€m') if market_val[1].find('span') else '-'
        end_val = re.findall(r"\€[^\]]+", market_val_end)

        end_val = end_val[0].strip('€m') if len(end_val) else '-'

        if ("Th." in start_val):
            start_val = start_val.strip("Th.")
            start_val = int(start_val) / 1000
            start_val  = str(start_val)
        

        if ("Th." in end_val):
            end_val = end_val.strip("Th.")
            end_val = int(end_val) / 1000
            end_val  = str(end_val)
        
        # change = float(end_val) - float(start_val)

        data = {
            "name": name,
            "year": year[y],
            "total_loan": rests[1].text,
            "average_loan (in years)": rests[2].text,
            "appearances": rests[3].text,
            "starting_formation": rests[4].text,
            "goals": rests[5].text,
            "average_minutes_played": rests[6].text,
            "market_value_at_start (in M €)": start_val,
            "market_value_at_end (in M €)": end_val,
            # "change_in_market_value (in M €)": change
        }

        club_data.append(data)

df = pd.DataFrame(club_data)
df.to_csv(f"../../dataset/DataCSV_{league}.csv", encoding='utf-8-sig', index=None)
df.to_excel(f"../../dataset/DataXLSX_{league}.xlsx", sheet_name='Data', encoding='utf-8-sig')
row, column = df.shape
print(f'total row: {row} & total column: {column}')