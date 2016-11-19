from fetcher import LeoFetcher
from parser import LeoParser
from parser import RateLimitException, ClientPoolRateException, UnknownErrorException
from database import MySqlDataSouce
from wordextractor import WordExtractor
import time

ENGLISH = "EN"
DEUTSCH = "DE"
NOUN = "NOUN"
SUCCESS = "SUCCESS"
ERROR_RATE_LIMIT = "ERROR RATE LIMIT"
ERROR_CLIENT_POOL ="ERROR CLIENT POOL"
ERROR_UKNOWN = "ERROR UKNOWN"
THROTTLE_SECONDS = 10
EXCEPTION_SLEEP_SECONDS = 60
ERROR_COUNT_SLEEP_SECONDS = 500

extractor = WordExtractor()
fetcher = LeoFetcher()
dao = MySqlDataSouce()
parser = LeoParser()

with open('resources/words.txt', 'r') as hall:
    data = hall.read()

words = extractor.get_words_from_text(data)
error_count = 0
for word in words :

    if error_count > 5 :
        print("Error count reached sleeping " + ERROR_COUNT_SLEEP_SECONDS+ " seconds")
        error_count = 0
        time.sleep(ERROR_COUNT_SLEEP_SECONDS)

    print("Searching for word: " + word)
    id = dao.add_search_history(word, ENGLISH)
    if id <= 0 :
        print("Adding search history record errored with : " + id)
        continue
    try:
        result = fetcher.search_english_word(ENGLISH, word)
        error_count = 0
    except RateLimitException as e:
        print("Rate Limit exeception fetching: %s %s", word,  e.message)
        dao.update_search_status_payload(id, ERROR_RATE_LIMIT, e.message)
        time.sleep(EXCEPTION_SLEEP_SECONDS)
        error_count += 1
        continue
    except ClientPoolRateException as e:
        print("Client pool exeception fetching: %s %s", word,  e.message)
        dao.update_search_status_payload(id, ERROR_CLIENT_POOL, e.message)
        time.sleep(EXCEPTION_SLEEP_SECONDS)
        error_count += 1
        continue
    except UnknownErrorException as e:
        print("Unknown error exeception fetching: %s %s", word,  e.message)
        dao.update_search_status_payload(id, ERROR_UKNOWN, e.message)
        time.sleep(EXCEPTION_SLEEP_SECONDS)
        error_count += 1
        continue


    translations = parser.extract_translation_nouns(result)
    print("Translations: " + str(translations))
    for trans in translations :
        englishWord = dao.find_english_word(trans["en"], NOUN)
        if englishWord :
            engId = englishWord[0]
        else:
            engId = dao.add_english_word(trans["en"], NOUN)

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
        deutschWord = dao.find_deutsch_word(trans["de"], NOUN)
        if deutschWord :
            deutId = deutschWord[0]
        else:
            deutId = dao.add_deutsch_word(trans["de"], NOUN, gender)
        dao.add_english_deutsch_translation(engId, deutId)
    dao.update_search_status(id, SUCCESS)
    time.sleep(THROTTLE_SECONDS)



