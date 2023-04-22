from helpers.request import Request

class Articles:
    def __init__(self):
        self.articles = []

    def scrapeArticles(self):
        print("Crawling articles...")

        # get the html
        req = Request()



