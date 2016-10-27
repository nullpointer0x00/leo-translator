import mysql.connector
from datetime import date, datetime, timedelta

class MySqlDataSouce:

    def __init__(self):
        self.config = {
            'user': 'leo',
            'password': 'leopass',
            'host': '127.0.0.1',
            'port' : '3406',
            'database': 'Uebersetzung',
            'raise_on_warnings': True,
        }
        self.cnx = mysql.connector.connect(**self.config)

    def __del__(self):
        try:
            self.cnx.close()
        except Exception as e:
            print("Error closing MySql connection: ", e)
            pass

    def add_search_history(self, searchTerm, lang):
        query = ("INSERT INTO SearchHistory "
                        "(SearchTerm, Lang) "
                        "VALUES (%s, %s)")
        data = (searchTerm, lang)
        return self.insert_record(query, data)

    def add_english_word(self, word, type) :
        query = ("INSERT INTO EnglishWord "
                      "(`Word`, `Type`) "
                      "VALUES (%s, %s)")
        data = (str(word), type)
        return self.insert_record(query, data)

    def add_deutsch_word(self, word, type, gender) :
        query = ("INSERT INTO DeutschWord "
                      "(`Word`, `Type`, `Gender`) "
                      "VALUES (%s, %s, %s)")
        data = (str(word), type, gender)
        return self.insert_record(query, data)

    def find_english_word(self, word, type):
        cursor = self.cnx.cursor()
        type ="NOUN"
        query = ("SELECT * FROM EnglishWord where `Word` = %s and `Type` = %s")
        data = (str(word), str(type))
        cursor.execute(query, data)
        rows = cursor.fetchall()
        if len(rows) is not 0 :
            return rows[0]

    def find_deutsch_word(self, word, type):
        cursor = self.cnx.cursor()
        query = ("SELECT * FROM DeutschWord where `Word` = %s and `Type` = %s")
        data = (str(word), str(type))
        cursor.execute(query, data)
        rows = cursor.fetchall()
        if len(rows) is not 0 :
            return rows[0]

    def add_english_deutsch_translation(self, englishWordId, deutschWordId):
        query = ("INSERT INTO EnglishDeutschTranslation "
                            "(`EnglishWordId`, `DeutschWordId`) "
                            "VALUES (%s, %s)")
        data = (englishWordId, deutschWordId)
        return self.insert_record(query, data)


    def insert_record(self, query, data):
        try :
            cursor = self.cnx.cursor()
            cursor.execute(query, data)
            id = cursor.lastrowid
            self.cnx.commit()
            return id
        except Exception :
            return -1