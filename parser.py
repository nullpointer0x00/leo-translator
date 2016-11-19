from lxml import html
class LeoParser:

    def __init__(self):
        print("Initiated")

    def extract_translation_nouns(self, xml):
        tree = html.fromstring(xml)
        self.validate(tree)
        nouns = tree.xpath("//section[@sctnum='0']/entry")
        results = []
        for noun in nouns :
            eng =  noun.xpath("./side[@lang='en']/words/word")
            engWord = eng[0].text_content()
            de = noun.xpath("./side[@lang='de']/words/word")
            deWord = de[0].text_content()
            results.append({"en" : engWord, "de": deWord})
        return results

    def validate(self, tree):
        self.is_rate_limited(tree)
        self.is_client_pool_rate(tree)
        self.is_unknown_error(tree)

    def is_rate_limited(self, tree):
        node = tree.xpath("//dictqueryerror[@errortype='clientRate']")
        if len(node) > 0 :
            raise RateLimitException(html.tostring(tree, pretty_print=True))

    def is_client_pool_rate(self, tree):
        node = tree.xpath("//dictqueryerror[@errortype='clientPoolRate']")
        if len(node) > 0:
            raise ClientPoolRateException(html.tostring(tree, pretty_print=True))

    def is_unknown_error(self, tree):
        node = tree.xpath("//dictqueryerror")
        if len(node) > 0:
            raise UnknownErrorException(html.tostring(tree, pretty_print=True))

class ClientPoolRateException(Exception):

    def __init__(self, message):
        self.message = message

class RateLimitException(Exception):

    def __init__(self, message):
        self.message = message

class UnknownErrorException(Exception):

    def __init__(self, message):
        self.message = message