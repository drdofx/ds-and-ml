from scrapers.issue import Issue
from scrapers.articles import Articles

def main():
    # scrape issues
    issue = Issue()
    issue.scrapeIssues()

    # scrape articles
    articles = Articles()
    articles.scrapeArticles()

    
if __name__ == "__main__":
    main() 