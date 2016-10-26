from fetcher import LeoFetcher
from parser import LeoParser
from database import MySqlDataSouce
from wordextractor import WordExtractor
import time

extractor = WordExtractor()
fetcher = LeoFetcher()
dao = MySqlDataSouce()
parser = LeoParser()

with open('resources/words.txt', 'r') as hall:
    data = hall.read()

words = extractor.get_words_from_text(data)

for word in words :
    print("Searching for word: " + word)
    dao.add_search_history(word, "EN")
    result = fetcher.search_english_word("EN", word)
    translations = parser.extract_translation_nouns(result)
    print("Translations: " + str(translations))
    for trans in translations :
        englishWord = dao.find_english_word(trans["en"], "NOUN")
        if englishWord :
            endId = englishWord[0]
        else:
            engId = dao.add_english_word(trans["en"], "NOUN")

        genderNounSplit = trans["de"].split(" ")
        if len(genderNounSplit) > 2 :
            print("We have a larger split: " + trans["de"])
        gender = "?"
        if genderNounSplit[0] == "der" :
            gender = "M"
        elif genderNounSplit[0] == "die" :
            gender = "F"
        elif genderNounSplit[0] == "das" :
            gender = "N"
        deutschWord = dao.find_deutsch_word(trans["de"], "NOUN" )
        if deutschWord :
            deutId = deutschWord[0]
        else:
            deutId = dao.add_deutsch_word(trans["de"], "NOUN", gender)
        dao.add_english_deutsch_translation(engId, deutId)
    time.sleep(2)



