import sqlite3

class Database:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.curr = self.conn.cursor()
        self.curr.execute("CREATE TABLE IF NOT EXISTS expense_record (item_name, item_price float, purchase_date date)")
        self.conn.commit()

    def fetchRecord(self, query): # query lets user pass any query to pass information
        self.curr.execute(query)
        rows = self.curr.fetchball()
        return rows 

    def insertRecord(self, item_name, item_price, purchase_date):
        self.curr.execute("INSERT INTO expense_record  VALUES (?,?,?)", (item_name, item_price, purchase_date))
        self.conn.commit()

    def removeRecord(self, rwid):
        self.curr.execute("DELETE FROM expense_record WHERE rwid =?", (rwid,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()