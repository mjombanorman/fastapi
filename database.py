# database.py
import sqlite3
from schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
class Database:
    def __init__(self):
        # create a SQLite database connection
        self.conn = sqlite3.connect("sqlite.db",check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_table("shipment")
        # create a table if it does not exist
    def create_table(self, name: str):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS shipment (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            content TEXT,
                            weight REAL,
                            status TEXT)""")
        self.conn.commit()

    def create(self, shipment: ShipmentCreate)-> int:
        #find new id from shipment table
        self.cur.execute("select MAX(id) from shipment")
        result = self.cur.fetchone()
        new_id = result[0] + 1 if result[0] is not None else 1

        self.cur.execute("""INSERT INTO shipment (id,content, weight, status)
                         VALUES (:id,:content,:weight,:status)""",
                         {
                             "id": new_id,
                             **shipment.model_dump(),
                               "status": "placed"
                         }
                       )
        self.conn.commit()
        return new_id

    def get(self, id: int)->ShipmentRead | None:
        self.cur.execute("SELECT * FROM shipment WHERE id = ?", (id,))
        row = self.cur.fetchone()
        return ShipmentRead.model_validate({
            "id": row[0],
            "content": row[1],
            "weight": row[2],
            "status": row[3]
        }) if row else None

    def update(self, id: int, shipment: ShipmentUpdate)-> ShipmentRead | None:
        self.cur.execute("""UPDATE shipment 
                         SET content = :content, 
                         weight = :weight, 
                         status = :status 
                         WHERE id = :id""",
                         {
                             "id": id,
                             **shipment.model_dump(exclude_unset=True)
                         })
        self.conn.commit()
        return self.get(id)

    def delete(self, id: int):
        self.cur.execute("DELETE FROM shipment WHERE id = ?", (id,))
        self.conn.commit()
       
    def close(self):
        self.conn.close()

   