import re

class WordExtractor:

    def __init__(self):
        print("Initiated")

    def get_words_from_text(self, text):
        text = re.sub(r'\W+', ' ', text)
        words = text.strip().split(' ')
        return words