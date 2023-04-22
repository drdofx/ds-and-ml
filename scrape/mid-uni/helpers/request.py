from bs4 import BeautifulSoup
import requests

class Request:
    def __init__(self):
        self.HEADERS = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        
    def getHtml(self, url):
        # get the html
        req = requests.get(url, headers=self.HEADERS)
        html = req.content

        return html

    def parseHtml(self, url):
        # get the html
        html = self.getHtml(url)

        # parse the html
        soup = BeautifulSoup(html, 'html.parser')

        return soup