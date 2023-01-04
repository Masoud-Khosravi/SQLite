import sqlite3


class DataBase:

    def __init__(self, db_name):
        self.db = db_name
        self._connect()
        self.__create_first()

    def _connect(self):
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()
        self._set_foreign_keys()

    def __create_first(self):
        pass

    def _set_foreign_keys(self):
        self.conn.execute("PRAGMA FOREIGN_KEYS = ON")