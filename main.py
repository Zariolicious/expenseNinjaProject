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

def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date..get())

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}') #dopvar is the widget where the current date is displayed

def clearEntries():
    item_name.delete(0,'end')
    item_amt.delete(0,'end')
    transaction_date.delete(0,'end')

def fetchRecords():
    f = data.fetchRecord('select rowid, *from expense_record')
    global count 
    for rec in f:
        tv.insert(parent=", index='0',iid=count, values=(rec[0], rec[1], rec[2], rec[3]))")
        count += 1
    tv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = tv.focus()
    val = tv.item(selected, 'values')

    try: 
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass


#GUI PART -------------------------------

ws = Tk()
ws.title('Expense Tracker')

#font 
f = ('Times new roman', 14,)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

ws.mainloop()

# Frame widget / display of data
f2 = Frame(ws)
f2.pack()

#Recording data 
f1 = Frame(
    ws, 
    padx=10
    pady=10
)
f1.pack(expand=True, fill=BOTH)

#Label widget
Label(f1, text = "ITEM NAME", font=f).grid(row=0, column=0, sticky=W)
Label(f1, text = "ITEM PRICE", font=f).grid(row=1, column=0, sticky=W)
Label(f1, text = "PURCHASE DATE", font=f).grid(row=2, column=0, sticky=W)

#entry grid 
item_name = Entry(f1, font=1)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

#grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))

#Action buttons
cur_date = Button(
    f1, 
    text = "Current Date", 
    font=f,
    bg = '#1F51FF', 
    command=setDate,
    width=15
)

submit_btn = Button(
    f1, 
    text='Save Record', 
    font=f
    command=saveRecord,
    bg= '#D9B036', 
    fg='white'
)

clr_btn = Button(
    f1, 
    text='Clear Entry',
    font=f,
    command=clearEntries,
    bg= '#D9B036', 
    fg='white'
)
 quit_btn = Button(
    f1, 
    text='Exit',
    font=f
    command=lambda:ws.destroy(),
    bg='#D33532',
    fg='white'
 )