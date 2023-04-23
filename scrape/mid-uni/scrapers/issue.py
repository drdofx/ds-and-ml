from helpers.request import Request
from helpers.store import Store
import json

class Issue:
    def __init__(self):
        self.start_url = "https://ojs.unikom.ac.id/index.php/komputika/issue/archive"
        self.request = Request()
        self.store = Store()
        
        try:
            # read issues.json
            with open('output/json/issues.json') as json_file:
                self.issues = json.load(json_file)
        except:
            self.issues = []

    def scrapeIssues(self):
        print("Scraping issues...")

        if len(self.issues) > 0:
            print("Issues already scraped!\n")
            return

        # send request and parse html
        soup = self.request.getSoup(self.start_url)

        # find all issues
        issue = soup.find_all('div', {"class": "obj_issue_summary_series"})

        # get href
        for i in range(0, len(issue)):
            # find the first a tag
            a = issue[i].find('a')

            # find the series div tag
            series = issue[i].find('div', {"class": "series"}) 

            # get the issue name
            issue_name = series.text.strip() if series else a.text.strip()

            data = {
                "issue": issue_name,
                "url": a['href']
            }

            self.issues.append(data)

        # store json
        store_json = self.store.storeJson(self.issues, "output/json/issues.json")

        print("Scraping issues done!\n") if store_json else print("Scraping issues failed!\n")


