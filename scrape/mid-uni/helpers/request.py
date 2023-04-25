from bs4 import BeautifulSoup
import requests
from pathlib import Path

class Request:
    def __init__(self):
        self.HEADERS = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
        
    def getHtml(self, url):
        # get the html
        req = requests.get(url, headers=self.HEADERS)
        html = req.content

        return html

    def getSoup(self, url):
        # get the html
        html = self.getHtml(url)

        # parse the html
        soup = BeautifulSoup(html, 'html.parser')

        return soup

    def getFile(self, url, filename):
        # modify the url
        url = self.modifyUrlForDownload(url)

        # get the response
        res = self.getHtml(url)

        # set path
        path = Path(f"output/pdf/{filename}.pdf")

        # write to file
        path.write_bytes(res)
        
        return path

    def modifyUrlForDownload(self, url):
        # modify the url
        url = url.replace("view", "download")

        return url