from helpers.request import Request
from helpers.store import Store
import json
import time


class ArticleDetail:
    def __init__(self):
        self.request = Request()
        self.store = Store()
        try:
            # read articles.json
            with open('output/json/articles.json') as json_file:
                self.articles = json.load(json_file)
        except Exception as e:
            print("Error: ", e)
            exit()

    def scrapeArticleDetails(self):
        print("Scraping article details...")
        
        if len(self.articles) > 0:
            print("Articles details already scraped!\n")
            return

        # scrape article details for each article in each issue
        for issue_name in self.articles:
            for article in self.articles[issue_name]:
                # skip if article detail already scraped
                if 'file_url' in article:
                    print(f"Article detail already scraped in article: {article['article_name']}!\n")

                    continue

                # scrape article details in an article
                self.scrapeArticleDetailsInAnArticle(article)

                # sleep for 1 second
                time.sleep(1)
            
            # store json of an issue 
            store_json = self.store.storeJson(self.articles, "output/json/articles.json")

            print(f"Scraping article details in issue: {issue_name} done!\n") if store_json else print(f"Scraping article details in issue: {issue_name} failed!\n")

        print("Scraping all article details done!\n")

    def scrapeArticleDetailsInAnArticle(self, article):
        print(f"Scraping article details in article: {article['article_name']}...")

        # send request and parse html
        soup = self.request.getSoup(article['url'])

        # find all articles
        article_detail = soup.find('a', {"class": "obj_galley_link pdf"})

        # return if article detail not found
        if not article_detail:
            print(f"Article detail not found in article: {article['article_name']}!\n")
            return

        # save article file url
        article['file_url'] = article_detail['href']
        print(f"Scraping article details in article: {article['article_name']} done!\n")

            
    
