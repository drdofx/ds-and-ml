import requests
from bs4 import BeautifulSoup
import json

class AllSquadPlayer:
    def __init__(self):
        self.HEADERS = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        self.clubs = []
        try:
            with open('json/clubs.json', 'r') as infile:
                self.clubs = json.load(infile)
        except:
            print("clubs.json is yet to be created")

        self.club_players = {}
        try:
            with open('json/club_players.json', 'r') as infile:
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
        with open('json/clubs.json', 'w') as outfile:
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
                
                nationality = values[i].find('img', {'class': 'flaggenrahmen'})['title']

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
        for i in range(0, len(self.clubs)):
            print("Progress: ", i+1, "/", len(self.clubs))
            self.scrapePlayers(self.clubs[i]['club'], self.clubs[i]['url'])

        # save to json file in json directory
        with open('json/club_players.json', 'w') as outfile:
            json.dump(self.club_players, outfile, indent=4)

    
        

# init class
all_squad_player = AllSquadPlayer()
all_squad_player.scrapeClubs()
# all_squad_player.scrapePlayers("Arsenal FC", "https://www.transfermarkt.com/fc-arsenal/startseite/verein/11/saison_id/2022")
all_squad_player.scrapeClubPlayers()



