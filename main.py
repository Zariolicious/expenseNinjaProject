from tkinter import *
from tkinter import ttk 
import datetime as dt #dates need to be extracted from computer
from mydb import * 
from tkinter import messagebox
import customtkinter as ctk 


#object for database 
data = Database(db='myexpense.db') #db is parameter from db class (name must have db extention) 

#global variables 
count = 0 
selected_rowid = 0 

def submit_balance():
    global desired_balance #declate as global to use it later
    desired_balance = balance_entry.get()
    try:
        desired_balance = float(desired_balance) #converts input to float
        messagebox.showinfo("Success", f"Desired balance set to: {desired_balance}")
        prompt_window.destroy() #closes window after submit
    except ValueError:
        messagebox.showerror("Error", "Please enter a number")

def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(), item_price=item_amt.get(), purchase_date=transaction_date.get())

def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}') #date of purchase is the widget where the current date is displayed

def clearEntries():
    item_name.delete(0,'end')
    item_amt.delete(0,'end')
    transaction_date.delete(0,'end')

def fetchRecords():
    f = data.fetchRecord('select rowid, *from expense_record')
    global count 
    for rec in f:
        tv.insert(parent='', index='0',iid=count, values=(rec[0], rec[1], rec[2], rec[3]))
        count += 1
    tv.after(400, refreshData) #in 400 milliseconds, shows new records added

def select_record(event):
    global selected_rowid
    selected = tv.focus() #lets us fetch the selected row
    val = tv.item(selected, 'values')

    try: 
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
    except Exception as ep:
        pass



def update_record():
    global selected_rowid

    selected = tv.focus() 
    #update the record
    try:
        data.updateRecord(namevar.get(), amtvar.get(), dopvar.get(), selected_rowid)
        tv.item(selected, text="", values=(namevar.get(), amtvar.get(), dopvar.get()))
    except Exception as ep:
        messagebox.showerror('Error', ep)
    
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    tv.after(400, refreshData)


def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")
    for i in f: 
        for j in i:
            if j is not None:
                total_expense = j
                remaining_balance = desired_balance - total_expense
                messagebox.showinfo('Current Balance: ', f"Total Expense: {j} \nBalance Remaining: {remaining_balance}") 
            else: 
                messagebox.showinfo('Current Balance: ', f"Total Expense: 0 \nDesired Balance: {desired_balance}")

def refreshData():
    for item in tv.get_children():
        tv.delete(item)
    fetchRecords() #displays items

def deleteRow():
    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()

#GUI PART -------------------------------

ws = Tk()
ws.title('Expense Ninja')

prompt_window = ctk.CTk()
prompt_window.title('Balance Setting')
prompt_window.geometry('400x400')


prompt_frame = ctk.CTkFrame(prompt_window)
prompt_frame.pack()

balance_label = ctk.CTkLabel(
    prompt_frame, 
    text="Enter your desired balance: ",
    fg_color=('#89CFF0', 'red'),
    corner_radius = 10, 
    )
balance_label.grid(row=0, column=0, sticky=W)


balance_entry = ctk.CTkEntry(prompt_frame)
balance_entry.grid(row=0, column=1)


#font 
f = ('Comic Sans MS', 14,)
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()

#Button to submit balance

prompt_submit_btn = ctk.CTkButton(
    prompt_frame, 
    text ="Submit",
    font=f,
    bg_color = '#1F51FF', 
    command=submit_balance,
    width=15
)


# Frame / display of data
f2 = Frame(ws)
f2.pack()

#Recording data 
f1 = Frame(
    ws, 
    padx=10,
    pady=10,
)
f1.pack(expand=True, fill=BOTH)

#
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
    font=f,
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
    font=f,
    command=lambda:ws.destroy(),
    bg='#D33532',
    fg='white'
 )

#maybe delete due to gridding
total_bal = Button(
    f1, 
    text='Total Balance',
    font=f,
    bg='#486966',
    command=totalBalance
 )

update_btn = Button(
    f1, 
    text='Update',
    bg='#C2BB00',
    command=update_record,
    font=f
 )

del_btn = Button(
    f1, 
    text='Delete',
    bg='#BD2A2E',
    command=deleteRow,
    font=f
 )

#Label widget
Label(f1, text = "ITEM NAME", font=f).grid(row=0, column=0, sticky=W)
Label(f1, text = "ITEM PRICE", font=f).grid(row=1, column=0, sticky=W)
Label(f1, text = "PURCHASE DATE", font=f).grid(row=2, column=0, sticky=W)

#entry widgets 
item_name = Entry(f1, font=1, textvariable=namevar)
item_amt = Entry(f1, font=f, textvariable=amtvar)
transaction_date = Entry(f1, font=f, textvariable=dopvar)

#entry grid placement
item_name.grid(row=0, column=1, sticky=EW, padx=(10, 0))
item_amt.grid(row=1, column=1, sticky=EW, padx=(10, 0))
transaction_date.grid(row=2, column=1, sticky=EW, padx=(10, 0))


#viewing widget
tv = ttk.Treeview(f2, columns=(1, 2, 3, 4), show ='headings', height=8)
tv.pack(side="left")

#treeview headings
tv.column(1, anchor=CENTER, stretch=NO, width=70)
tv.column(2, anchor=CENTER)
tv.column(3, anchor=CENTER)
tv.column(4, anchor=CENTER)
tv.heading(1, text="Serial no")
tv.heading(2, text="Item Name", )
tv.heading(3, text="Item Price")
tv.heading(4, text="Purchase Date")

#binding treeview
tv.bind("<ButtonRelease-1>", select_record)

#treeview style
style = ttk.Style()
style.theme_use("default")
style.map("Treeview")

#scrollbar widget
scrollbar = Scrollbar(f2, orient='vertical')
scrollbar.configure(command=tv.yview)
scrollbar.pack(side="right", fill="y")
tv.config(yscrollcommand=scrollbar.set)

#button grid placement

cur_date.grid(row=3, column=1, sticky=EW, padx=(10, 0))
submit_btn.grid(row=0, column=2, sticky=EW, padx=(10, 0))
clr_btn.grid(row=1, column=2, sticky=EW, padx=(10, 0))
quit_btn.grid(row=2, column=2, sticky=EW, padx=(10, 0))
total_bal.grid(row=0, column=3, sticky=EW, padx=(10, 0))
update_btn.grid(row=1, column=3, sticky=EW, padx=(10, 0))
del_btn.grid(row=2, column=3, sticky=EW, padx=(10, 0))
prompt_submit_btn.grid(row=1, columnspan=2, pady=10) #pf frame


prompt_window.mainloop()
ws.mainloop()
