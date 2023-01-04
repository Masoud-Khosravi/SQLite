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
        self.__create_user()
        self.__create_categories()
        self.__create_brands()
        self.__create_wares()
        self.__create_sells()
        self.__create_buys()
        self.__create_sells_details()
        self.__create_buys_details()
        self._add_first_values()
        self.conn.commit()
        self.conn.close()

    def _set_foreign_keys(self):
        self.conn.execute("PRAGMA FOREIGN_KEYS = ON")

    def view_wares(self, brand_id, category_id):
        self._connect()
        query = "SELECT * FROM Wares WHERE Brand_ID={} AND Category_ID={}".format(brand_id, category_id)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def view_buys(self):
        self._connect()
        # self.cursor.execute("SELECT * FROM Buys")
        query = "SELECT B.ID,B.Total_amount,U.Name || ' ' || U.Family As FullName ,B.Date FROM" \
                " Buys B INNER JOIN Users U ON B.User_ID = U.ID"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def view_sells(self):
        self._connect()
        query = "SELECT S.ID,S.Total_amount,U.Name || ' ' || U.Family As FullName ,S.Date FROM" \
                " Sells S INNER JOIN Users U ON S.User_ID = U.ID"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def view_brands(self):
        self._connect()
        self.cursor.execute("SELECT * FROM Brands")
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def view_sellers(self):
        self._connect()
        self.cursor.execute("SELECT * FROM Users WHERE Is_Seller=1")
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def view_customers(self):
        self._connect()
        self.cursor.execute("SELECT ID, Name || ' ' || Family AS Customer FROM Users WHERE Is_Seller=0")
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def view_categories(self):
        self._connect()
        self.cursor.execute("SELECT * FROM Categories")
        rows = self.cursor.fetchall()
        self.conn.close()
        return rows

    def get_sell_price(self, ware_id):
        self._connect()
        query = "SELECT Sell_Price FROM Wares WHERE ID={}".format(ware_id)
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        self.conn.close()
        if len(rows) > 0:
            rows = rows[0][0]
        else:
            rows = 0
        return rows

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

    def _add_first_values(self):

        # ================ Check All items if exist or earlier exist anything --> do nothing ================
        # ================ Means just add item in first time create database ================================
        query = "SELECT * FROM sqlite_sequence"
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        category_exist = False
        brand_exist = False
        user_exist = False
        ware_exist = False
        for items in res:
            if 'Categories' in items:
                category_exist = True
            elif 'Brands' in items:
                brand_exist = True
            elif 'Users' in items:
                user_exist = True
            elif 'Wares' in items:
                ware_exist = True

        if not category_exist:
            # =================== Create Some Categories ========================
            categories = [("Other",), ("Shows",), ("Shirts",), ("Jeans",)]
            #         id->    1     ,      2    ,      3      ,    4
            self.cursor.executemany("INSERT INTO Categories(Name) VALUES (?)", categories)

        if not brand_exist:
            # =================== Create Some Brands ============================
            #           Name,          Address,  Website ,Phone, Email
            brands = [("Other Brand", "No Address", None, None, None),  # id->1
                      ("Adidas", "US Address", "adidas.com", "+1-12345", "info@adidas.com"),  # id->2
                      ("Nike", "US2 Address", "nike.com", "+1-67890", "info@nike.com"),  # id->3
                      ("Puma", "Germany Address", "puma.com", "+49-000111", "info@puma.com")]  # id->4

            self.cursor.executemany("INSERT INTO Brands(Name,Address,Website,Phone,Email) VALUES (?,?,?,?,?)", brands)

        if not ware_exist:
            # =================== Create Some Wares ============================
            #         Name, Brand_ID,Category_ID
            Wares = [("Ad_Shoes_1", 2, 2), ("Ad_Shoes_2", 2, 2), ("Ad_Shoes_3", 2, 2),
                     ("Ad_Shirt_1", 2, 3), ("Ad_Shirt_2", 2, 3), ("Ad_Shirt_3", 2, 3),
                     ("Ni_Shoes_N1", 3, 2), ("Ni_Shoes_N2", 3, 2), ("Ni_Shoes_N3", 3, 2),
                     ("Ni_Shirt_S1", 3, 3), ("Ni_Shirt_S2", 3, 3), ("Ni_Shirt_S3", 3, 3),
                     ("Ni_Jeans_J1", 3, 4), ("Ni_Jeans_J2", 3, 4), ("Ni_Jeans_J3", 3, 4),
                     ("Pu_Shoes_1", 4, 2), ("Pu_Shoes_2", 4, 2), ("Pu_Shoes_3", 4, 2),
                     ("Pu_Shirt_1", 4, 3), ("Pu_Shirt_1", 4, 3), ("Pu_Shirt_1", 4, 3),
                     ("Pu_Jeans_1", 4, 4), ("Pu_Jeans_2", 4, 4), ("Pu_Jeans_3", 4, 4)]

            self.cursor.executemany("INSERT INTO Wares(Name,Brand_ID,Category_ID) VALUES (?,?,?)", Wares)

        if not user_exist:
            # =================== Create Some Sellers ===========================
            #           Name,   Family,  Sex, Address, Phone, Is_Seller
            Sellers = [("Other", "", 1, "Other Address", None, 1),
                       ("Masoud", "Khosravi", 1, "Germany", "+4912345678", 1),
                       ("John", "Snow", 1, "England", "+44111222333", 1)]

            # =================== Create Some Customers ===========================
            #              Name,   Family,  Sex, Address, Phone, Is_Seller
            Customers = [("Other", "", 1, "Other Address", None, 0),
                         ("Masoud", "Khosravi", 1, "Iran", "+98123456789", 0),
                         ("Jack", "Bower", 1, "England", "+44888999000", 0),
                         ("Mary", "Elfi", 0, "US Street", "+1000111222", 0),
                         ("Anje", "Joli", 0, "Hollywood", "+9988776655", 0)]

            self.cursor.executemany("INSERT INTO Users(Name,Family,Sex,Address,Phone,Is_Seller) VALUES (?,?,?,?,?,?)",
                                    Sellers)
            self.cursor.executemany("INSERT INTO Users(Name,Family,Sex,Address,Phone,Is_Seller) VALUES (?,?,?,?,?,?)",
                                    Customers)

# db = DataBase('Sale_DB.db')
