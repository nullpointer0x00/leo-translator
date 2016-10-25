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

    def add_search_history(self, searchTerm, lang):
        cursor = self.cnx.cursor()
        add_search = ("INSERT INTO SearchHistory "
                        "(SearchTerm, Lang) "
                        "VALUES (%s, %s)")
        search_data = (searchTerm, lang)
        cursor.execute(add_search, search_data)
        search_id = cursor.lastrowid
        self.cnx.commit()
        return search_id

