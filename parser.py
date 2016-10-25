from lxml import html
class LeoParser:

    def __init__(self):
        print("Initiated")

    def extract_translation_nouns(self, xml):
        tree = html.fromstring(xml)
        nouns = tree.xpath("//section[@sctnum='0']/entry")
        results = []
        for noun in nouns :
            eng =  noun.xpath("./side[@lang='en']/words/word")
            engWord = eng[0].text_content()
            de = noun.xpath("./side[@lang='de']/words/word")
            deWord = de[0].text_content()
            results.append({"en" : engWord, "de":deWord})
        return results

