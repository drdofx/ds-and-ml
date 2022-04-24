import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import time

"""
Scrape the transfermarkt.com website for out on loan players data from each club in the top 4 league from season 2004-2020

Page info: 	This statistic shows the performance data of all players in this season who had a loan spell with a club from this competition.
"""

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

year = [2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]


leagues = {
    "GB1": "Premier League",
    "ES1": "La Liga",
    "IT1": "Serie A",
    "L1": "Bundesliga",
}

for key in leagues:
    club_data = []
    for y in range(0, len(year)):
        url = f"https://www.transfermarkt.com/premier-league/leihspieler/wettbewerb/{key}/plus/1?saison_id={year[y]}&leihe=ist"    

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
    df.to_csv(f"../../dataset/loan_player_data/DataCSV_{leagues[key]}.csv", encoding='utf-8-sig', index=None)
    df.to_excel(f"../../dataset/loan_player_data/DataXLSX_{leagues[key]}.xlsx", sheet_name='Data', encoding='utf-8-sig')
    row, column = df.shape
    print(f'For {leagues[key]} -> total row: {row} & total column: {column}')

    time.sleep(5)