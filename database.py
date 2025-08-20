# database.py
import sqlite3



class Database:
    def __init__(self):
        #create a SQLite database connection
        self.conn = sqlite3.connect("sqlite.db")
        self.cur = self.conn.cursor()
        self.create_table("shipment")
        #create a table if it does not exist
    def create_table(self,name:str):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS ? (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT,
                            weight REAL,
                            status TEXT)""",(name,))
        self.conn.commit()
