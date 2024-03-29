import json
import time

class ArticleDetail:
    def __init__(self, request, store, articles):
        self.request = request
        self.store = store
        self.articles = articles

        if len(self.articles) == 0:
            print("Articles not scraped yet!\n")
            return False

    def scrapeArticleDetails(self):
        print("Scraping article details...")
        
        has_article_detail = False

        # scrape article details for each article in each issue
        for issue_name in self.articles:
            for article in self.articles[issue_name]:
                # skip if article detail already scraped
                if 'file_url' in article:
                    # set has_article_detail to True
                    has_article_detail = True
                    continue

                # set has_article_detail to False
                has_article_detail = False

                # scrape article details in an article
                self.scrapeArticleDetailsInAnArticle(article)

                # sleep for 1 second
                time.sleep(1)
            
            # if has_article_detail is True, return
            if has_article_detail:
                print(f"Article details already scraped!\n")
                return self.articles

            # store json of articles 
            store_json = self.store.storeJson(self.articles, "output/json/articles.json")

            print(f"Scraping article details in issue: {issue_name} done!\n") if store_json else print(f"Scraping article details in issue: {issue_name} failed!\n")

        print("Scraping all article details done!\n")
        return self.articles

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

            
    
