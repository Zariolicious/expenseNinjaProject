import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.curr = self.conn.cursor()
        self.curr.execute("CREATE TABLE IF NOT EXISTS expense_record (item_name, item_price float, purchase_date date)")
        self.conn.commit()
#Fetches records based on string query input
    def fetchRecord(self, query): # query lets user pass any query to pass information
        self.curr.execute(query)
        rows = self.curr.fetchball()
        return rows 

#Inserts new record into expense_record table
    def insertRecord(self, item_name, item_price, purchase_date):
        self.curr.execute("INSERT INTO expense_record  VALUES (?,?,?)", (item_name, item_price, purchase_date))
        self.conn.commit()

    def removeRecord(self, rwid):
        self.curr.execute("DELETE FROM expense_record WHERE rwid =?", (rwid,))
        self.conn.commit()
#Destructor, closes connection to database
    def __del__(self):
        self.conn.close()