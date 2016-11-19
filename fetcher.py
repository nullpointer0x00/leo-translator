import requests
import datetime
from lxml import html

class LeoFetcher:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
    }

#http://dict.leo.org/dictQuery/m-vocab/ende/query.xml?tolerMode=nof&lp=ende&lang=en&rmWords=off&rmSearch=on&search=spider&searchLoc=0&resultOrder=basic&multiwordShowSingle=on&pos=0&sectLenMax=16&n=1&t=2016-11-01T03:16:11.373Z

    def __init__(self):
        self.baseUrl = "http://dict.leo.org/dictQuery/m-vocab/ende/query.xml"
        self.params = "?tolerMode=nof&lp=ende&lang={0}&rmWords=off&rmSearch=on&search={1}&searchLoc=0&resultOrder=basic&multiwordShowSingle=on&pos=0&sectLenMax=100&n=1&t={2}"

    def search_english_word(self, lang, word):
        session = requests.session()
        time = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%mZ")
        url = self.baseUrl + self.params.format(lang, word, time)
        print("Url %s", url)
        content = session.get(url, headers = self.headers).content
        print("---------Content-------------------")
        print(content)
        print("---------END-----------------------")
        return content