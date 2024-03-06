from tkinter import *
from tkinter import ttk 
import datetime as dt #dates need to be extracted from computer
from database import * 
from tkinter import messagebox

#object for database 
data = Database(db='myexpense.db') #db is parameter from db class (name must have db extention) 

#global variables 
count = 0 
selected_rowid = 0 


ws = Tk()
ws.title('Expense Tracker')


ws.mainloop()