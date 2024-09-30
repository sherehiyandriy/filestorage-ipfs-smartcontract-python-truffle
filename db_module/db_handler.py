import mysql.connector

class DBHandler:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("connected to database")
        self.cursor = self.conn.cursor()

    def store_file(self, file_name, cid):
        query = "INSERT INTO files (file_name, cid) VALUES (%s, %s)"
        self.cursor.execute(query, (file_name, cid))
        self.conn.commit()

    def retrieve_file(self, file_name):
        query = "SELECT cid FROM files WHERE file_name = %s"
        self.cursor.execute(query, (file_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    
    def store_dublicate(self, file_name, cid):
        query = "UPDATE files SET cid = %s WHERE file_name = %s"
        self.cursor.execute(query, (cid, file_name))
        self.conn.commit()