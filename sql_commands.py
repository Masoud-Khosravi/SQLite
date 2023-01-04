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

    def __create_user(self):
        query = "CREATE TABLE IF NOT EXISTS Users (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "Name varchar(30) NOT NULL," \
                "Family varchar(30)," \
                "Sex bit ," \
                "Address varchar(50)," \
                "Phone varchar(15)," \
                "Is_Seller bit NOT NULL ON CONFLICT REPLACE DEFAULT 0)"
        self.cursor.execute(query)

    def __create_categories(self):
        query = "CREATE TABLE IF NOT EXISTS Categories (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "Name varchar(30) NOT NULL)"
        self.cursor.execute(query)

    def __create_brands(self):
        query = "CREATE TABLE IF NOT EXISTS Brands (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "Name varchar(30) NOT NULL," \
                "Address varchar(100)," \
                "Website varchar(200)," \
                "Phone varchar(15)," \
                "Email varchar(50))"
        self.cursor.execute(query)

    def __create_wares(self):
        query = "CREATE TABLE IF NOT EXISTS Wares (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "Name varchar(30) NOT NULL," \
                "Brand_ID INTEGER NOT NULL," \
                "Category_ID INTEGER NOT NULL," \
                "Stock smallint NOT NULL ON CONFLICT REPLACE DEFAULT 0," \
                "Buy_Price money NOT NULL ON CONFLICT REPLACE DEFAULT 0," \
                "Sell_Price money NOT NULL ON CONFLICT REPLACE DEFAULT 0," \
                "FOREIGN KEY(Brand_ID) REFERENCES Brands(ID)," \
                "FOREIGN KEY(Category_ID) REFERENCES Categories(ID) )"
        self.cursor.execute(query)

    def __create_sells(self):
        query = "CREATE TABLE IF NOT EXISTS Sells (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "Total_amount money NOT NULL," \
                "User_ID INTEGER NOT NULL," \
                "[Date] datetime NOT NULL," \
                "FOREIGN KEY(User_ID) REFERENCES Users(ID) )"
        self.cursor.execute(query)
        query = "SELECT name FROM sqlite_sequence WHERE name='Sells'"
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res is None:  # Means its first time
            query = "INSERT INTO SQLITE_SEQUENCE VALUES ('Sells',100) "  # Start ID from 100
            self.cursor.execute(query)

    def __create_buys(self):
        query = "CREATE TABLE IF NOT EXISTS Buys (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "Total_amount money NOT NULL," \
                "User_ID int NOT NULL," \
                "[Date] datetime NOT NULL," \
                "FOREIGN KEY(User_ID) REFERENCES Users(ID))"
        self.cursor.execute(query)
        query = "SELECT name FROM sqlite_sequence WHERE name='Buys'"
        self.cursor.execute(query)
        res = self.cursor.fetchone()
        if res is None:  # Means its first time
            query = "INSERT INTO SQLITE_SEQUENCE VALUES ('Buys',100)"  # Start ID from 100
            self.cursor.execute(query)

    def __create_sells_details(self):
        query = "CREATE TABLE IF NOT EXISTS Sells_Details (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "ID_Sell int NOT NULL," \
                "Ware_ID int NOT NULL," \
                "Value smallint NOT NULL," \
                "Sell_Price money NOT NULL," \
                "Buy_Price money NOT NULL," \
                "FOREIGN KEY(ID_Sell) REFERENCES Sells(ID)," \
                "FOREIGN KEY(Ware_ID) REFERENCES Wares(ID))"
        self.cursor.execute(query)

    def __create_buys_details(self):
        query = "CREATE TABLE IF NOT EXISTS Buys_Details (" \
                "ID INTEGER PRIMARY KEY AUTOINCREMENT," \
                "ID_Buy int NOT NULL," \
                "Ware_ID int NOT NULL," \
                "Value smallint NOT NULL," \
                "Price money NOT NULL," \
                "FOREIGN KEY(ID_Buy) REFERENCES Buys(ID)," \
                "FOREIGN KEY(Ware_ID) REFERENCES Wares(ID))"
        self.cursor.execute(query)
