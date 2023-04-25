from helpers.request import Request
from helpers.store import Store
import json
import time

class ArticleFile:
    def __init__(self):
        self.request = Request()
        self.store = Store()

        try:
            # read articles.json
            with open('output/json/articles.json') as json_file:
                self.articles = json.load(json_file)
        except Exception as e:
            print("Error", e)
            exit()

    def downloadArticle(self):
        print("Downloading articles...")

        # download article for each article in each issue
        for issue_name in self.articles:
            for article in self.articles[issue_name]:
                # skip if file_path not in article
                if 'file_url' not in article:
                    print(f"Article file url not found in article: {article['article_name']}!\n")
                    continue

                # download article file in an article
                file_path = self.downloadArticlePdf(article['file_url'])

                # skip if file already exists
                if not file_path:
                    continue

                # add file_path to article
                article['file_path'] = file_path

                # sleep for 1 second
                time.sleep(1)

                print(f"Downloading article pdf in article: {article['article_name']} done!\n")

            store_json = self.store.storeJson(self.articles, "output/json/articles.json")

            print(f"Downloading article pdf in issue: {issue_name} done!\n") if store_json else print(f"Downloading article pdf in issue: {issue_name} failed!\n")

        print("Downloading all articles done!\n")

    def downloadArticlePdf(self, article_url):
        print(f"Downloading article: {article_url}...")

        # get file_name
        file_name = article_url.split('/')[-1]

        # check if file already exists
        full_file_path = f"output/pdf/{file_name}.pdf"
        if self.store.checkFileExists(full_file_path):
            print(f"File already exists in {full_file_path}!\n")
            return False

        # send request and download file
        path = self.request.getFile(article_url, file_name)

        print(f"Downloading article done! File saved to {path}\n") if path else print(f"Downloading article failed!\n")

        return path
