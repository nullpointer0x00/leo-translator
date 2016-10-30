import requests
from lxml import html

class LeoFetcher:

    headers = {
        'User-Agent': 'Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0',
    }


    def __init__(self):
        self.session = requests.session()
        self.baseUrl = "http://dict.leo.org/dictQuery/m-vocab/ende/query.xml"
        self.params = "?tolerMode=nof&lp=ende&lang={0}&rmWords=off&rmSearch=on&search={1}&searchLoc=0&resultOrder=basic&multiwordShowSingle=on&pos=0&sectLenMax=100&n=1"

    def search_english_word(self, lang, word):
        url = self.baseUrl + self.params.format(lang, word)
        return self.session.get(url, headers = self.headers).content