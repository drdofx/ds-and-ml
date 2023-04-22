from scrapers.issue import Issue
from helpers.store import Store

def main():
    issue = Issue()
    issues = issue.scrapeIssues()

    store = Store()
    store.storeJson(issues, "issues.json")

if __name__ == "__main__":
    main() 