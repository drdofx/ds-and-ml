from scrapers.issue import Issue
from scrapers.article import Article
from scrapers.article_detail import ArticleDetail
from scrapers.article_file import ArticleFile

def main():
    # scrape issues
    issue = Issue()
    issue.scrapeIssues()

    # scrape article
    article = Article()
    article.scrapeArticles()

    # scrape article details
    article_detail = ArticleDetail()
    article_detail.scrapeArticleDetails()

    # download article files
    article_file = ArticleFile()
    article_file.downloadArticle()

    
if __name__ == "__main__":
    main() 