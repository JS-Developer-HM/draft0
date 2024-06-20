import mysql.connector

user = "root"
password = "Sim12345"
host = "localhost"
database = "face_recognition"

class MySqlConnection:
    def __init__(self):
        self.connect = mysql.connector.connect(
            user = user,
            password = password,
            host = host,
            database = database
        )
        self.cursor = self.connect.cursor();
        


    def insert(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.connect.commit()

    def read(self, sql_query):
        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()
        return rows

    def create(self, sql_query):
        self.cursor.execute(sql_query)
        self.connect.commit()

    def update(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.connect.commit()

    def delete(self, sql_query, values):
        self.cursor.execute(sql_query, values)
        self.connect.commit()

    def close(self):
        self.cursor.close()
        self.connect.close()


db = MySqlConnection()
# dbCursor = db.connect.cursor();