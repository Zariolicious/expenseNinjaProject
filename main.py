import sqlite3

class Database:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.curr = self.conn.cursor()
        self.curr.execute("CREATE TABLE IF NOT EXISTS expense_record (item_name, item_price float, purchase_date date)")
        self.conn.commit()