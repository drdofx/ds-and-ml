import requests
from bs4 import BeautifulSoup
import json
import time
import xlsxwriter

class AllSquadPlayer:
    def __init__(self):
        self.HEADERS = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        self.clubs = []
        try:
            with open('output/json/clubs.json', 'r') as infile:
                self.clubs = json.load(infile)
        except:
            print("clubs.json is yet to be created")

        self.club_players = {}
        try:
            with open('output/json/club_players.json', 'r') as infile:
                self.club_players = json.load(infile)
        except:
            print("club_players.json is yet to be created")

    def scrapeClubs(self):
        # return if clubs.json is already exist
        if len(self.clubs) > 0:
            print("clubs.json is already exist")
            return

        url = "https://www.transfermarkt.com/premier-league/startseite/wettbewerb/GB1"

        req = requests.get(url, headers=self.HEADERS)
        page_soup = BeautifulSoup(req.content, 'html.parser')

        values = page_soup.find_all('td', {"class": "hauptlink no-border-links"})

        try:
            for i in range(0, len(values)):
                # print progress
                print("Progress: ", i+1, "/", len(values))

                # get the first a tag text
                a_values = values[i].find('a')
                
                club = a_values.text
                club_url = a_values['href']

                club_url = "https://www.transfermarkt.com" + club_url

                data = {
                    "club": club,
                    "url": club_url
                }
                
                print(data)

                self.clubs.append(data)                
        except:
            print("Error: ", club)

        # save to json file in json directory
        with open('output/json/clubs.json', 'w') as outfile:
            json.dump(self.clubs, outfile, indent=4)

    def scrapePlayers(self, club_name, club_url):
        req = requests.get(club_url, headers=self.HEADERS)
        page_soup = BeautifulSoup(req.content, 'html.parser')

        values = page_soup.find_all('tr', {"class": ['odd', 'even']})

        try:
            for i in range(0, len(values)):
                number = values[i].find('td', {'class': "zentriert"}).text
                
                name = values[i].find('div', {'class': 'di nowrap'}).text
                
                position = values[i].find('table', {'class': 'inline-table'}).findAll("tr")[1].text

                date_of_birth = values[i].findAll('td', {'class': 'zentriert'})[1].text

                # example of date_of_birth: May 30, 1999 (23)
                # split by ( and get the first element for dob and second element for age
                dob, age = date_of_birth.split(" (")
                age = age[:-1]
                
                nationality = values[i].findAll('img', {'class': 'flaggenrahmen'})
                # loop through nationality, get the title and join it with a comma
                nationality = ", ".join([n['title'] for n in nationality])
            
                market_val = values[i].find('td', {'class': 'rechts hauptlink'}).text
                market_val = market_val.replace(u'\xa0', '')

                data = {
                    "squad_number": number,
                    "name": name,
                    "position": position,
                    "date_of_birth": dob,
                    "age": age,
                    "nationality": nationality,
                    "market_value": market_val
                }   

                if club_name not in self.club_players:
                    self.club_players[club_name] = []

                self.club_players[club_name].append(data)                

        except:
            print("Error: ", name)

        print(json.dumps(self.club_players, indent=4))


    def scrapeClubPlayers(self):
        # return if club_players.json is already exist
        if len(self.club_players) > 0:
            print("club_players.json is already exist")
            return
            
        for i in range(0, len(self.clubs)):
            print("Progress: ", i+1, "/", len(self.clubs))
            self.scrapePlayers(self.clubs[i]['club'], self.clubs[i]['url'])
            time.sleep(3)

        # save to json file in json directory
        with open('output/json/club_players.json', 'w') as outfile:
            json.dump(self.club_players, outfile, indent=4)

    def exportToXlsx(self):
        workbook = xlsxwriter.Workbook('output/xlsx/club_players.xlsx')
        bold = workbook.add_format({'bold': True})
        title = workbook.add_format({'align': 'center', 'font_size': 20, 'bold': True, 'bg_color': '#D7E4BC'})

        for club in self.club_players:
            worksheet = workbook.add_worksheet(club)

            worksheet.set_column('A:G', 20)

            worksheet.merge_range(0, 0, 0, 6, club, title)

            worksheet.write(1, 0, "Squad Number", bold)
            worksheet.write(1, 1, "Name", bold)
            worksheet.write(1, 2, "Position", bold)
            worksheet.write(1, 3, "Date of Birth", bold)
            worksheet.write(1, 4, "Age", bold)
            worksheet.write(1, 5, "Nationality", bold)
            worksheet.write(1, 6, "Market Value", bold)

            for i in range(0, len(self.club_players[club])):
                worksheet.write(i+2, 0, self.club_players[club][i]['squad_number'])
                worksheet.write(i+2, 1, self.club_players[club][i]['name'])
                worksheet.write(i+2, 2, self.club_players[club][i]['position'])
                worksheet.write(i+2, 3, self.club_players[club][i]['date_of_birth'])
                worksheet.write(i+2, 4, self.club_players[club][i]['age'])
                worksheet.write(i+2, 5, self.club_players[club][i]['nationality'])
                worksheet.write(i+2, 6, self.club_players[club][i]['market_value'])

        workbook.close()

        print("Export to xlsx is done")       
    
# init class
all_squad_player = AllSquadPlayer()
all_squad_player.scrapeClubs()
all_squad_player.scrapeClubPlayers()
all_squad_player.exportToXlsx()



