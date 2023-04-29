import json
import time

class ArticleFile:
    def __init__(self, request, store, articles):
        self.request = request
        self.store = store
        self.articles = articles

        if len(self.articles) == 0:
            print("Articles not scraped yet!\n")
            return False

    def downloadArticle(self):
        print("Downloading articles...")

        has_article_file = False

        # download article for each article in each issue
        for issue_name in self.articles:
            for article in self.articles[issue_name]:
                # skip if article file already downloaded
                if 'file_path' in article:
                    # set has_article_file to True
                    has_article_file = True
                    continue

                # download article file in an article
                file_path = self.downloadArticlePdf(article['file_url'])

                # skip if file already exists in output/pdf
                if not file_path:
                    has_article_file = True
                    continue

                # set has_article_file to False
                has_article_file = False

                # add file_path to article
                article['file_path'] = str(file_path)
                print(article)

                # sleep for 1 second
                time.sleep(1)

                print(f"Downloading article pdf in article: {article['article_name']} done!\n")


            # if has_article_file is True, return
            if has_article_file:
                print(f"Article files already downloaded!\n")
                return self.articles

            # store json of articles
            store_json = self.store.storeJson(self.articles, "output/json/articles.json")

            print(f"Downloading article pdf in issue: {issue_name} done!\n") if store_json else print(f"Downloading article pdf in issue: {issue_name} failed!\n")

        print("Downloading all articles done!\n")
        return self.articles

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
