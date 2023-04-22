from helpers.request import Request

class Issue:
    def __init__(self):
        self.start_url = "https://ojs.unikom.ac.id/index.php/komputika/issue/archive"
        self.issues = []

    def scrapeIssues(self):
        print("Crawling journal...")

        # get the html
        req = Request()

        # parse the html
        soup = req.parseHtml(self.start_url)

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

        return self.issues


