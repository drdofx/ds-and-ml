import time
import json

class Article:
    def __init__(self, request, store, issues):
        self.request = request
        self.store = store
        self.issues = issues

        if len(self.issues) == 0:
            print("Issues not scraped yet!\n")
            return False

        try:
            # read articles.json
            with open('output/json/articles.json') as json_file:
                self.articles = json.load(json_file)
        except:
            self.articles = {}
            self.article_count = 0

    def scrapeArticles(self):
        print("Scraping articles...")

        if len(self.articles) > 0:
            print("Articles already scraped!\n")
            return self.articles

        for i in range(0, len(self.issues)):
            issue_name = self.issues[i]['issue']
            issue_url = self.issues[i]['url']

            self.scrapeArticlesInAnIssue(issue_name, issue_url)

            time.sleep(3)

        print(f"Total articles: {self.article_count}\n")

        # store json
        store_json = self.store.storeJson(self.articles, "output/json/articles.json")

        if store_json:
            print("Storing articles json done!\n")
            return self.articles
        else:
            print("Storing articles json failed!\n")
            return False

    def scrapeArticlesInAnIssue(self, issue_name, issue_url):
        print(f"Scraping articles in issue {issue_name}...")

        # send request and parse html
        soup = self.request.getSoup(issue_url)

        # find all articles
        article = soup.find_all('h4', {"class": "issue-article-title card-title"})
        self.article_count += len(article)

        # get href
        for i in range(0, len(article)):
            # find the first a tag
            a = article[i].find('a')

            data = {
                "article_name": a.text.strip(),
                "url": a['href']
            }

            if issue_name not in self.articles:
                self.articles[issue_name] = []

            self.articles[issue_name].append(data)

        print(f"Scraping articles in issue {issue_name} done!\n")



