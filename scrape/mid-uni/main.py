import logging

from scrapers.issue import Issue
from scrapers.article import Article
from scrapers.article_detail import ArticleDetail
from scrapers.article_file import ArticleFile
from helpers.reader import Reader
from helpers.request import Request
from helpers.store import Store

class Application:
    def __init__(self, request, store):
        self.issue = Issue(request, store)
        self.article = Article(request, store, self.issue.issues)
        self.article_detail = ArticleDetail(request, store, self.article.articles)
        self.article_file = ArticleFile(request, store, self.article.articles)
        self.reader = Reader('output/pdf/1.pdf')

    def runScraping(self):
        logging.info("Scraping started")

        self.issue.scrapeIssues()
        self.article.scrapeArticles()
        self.article_detail.scrapeArticleDetails()
        self.article_file.downloadArticle()
            
        logging.info("Scraping finished")

    def runReading(self):
        logging.info("Reading started")

        text = self.reader.readPdf()
        print(text)

        logging.info("Reading finished")


def main():
    logging.basicConfig(filename='output/log/scraping.log', level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

    # Initialize Request and Store objects
    request = Request()
    store = Store()

    application = Application(request, store)
    application.runScraping()
    application.runReading()

if __name__ == "__main__":
    main() 