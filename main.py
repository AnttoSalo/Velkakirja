import tkinter as tk
import mariadb
import sys

try:
    conn = mariadb.connect(
        user="root",
        password="admin",
        host="localhost",
        port=3306,
        database="debts"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

window = tk.Tk()
frame = tk.Frame(window)
frame.pack()
window.geometry("800x600")

def submit():
 
    name=name_var.get()
    money=money_var.get()
     
    print("The name is : " + name)
    print("The money is : " + money)
     
    name_var.set("")
    money_var.set("")
    cur.execute(
    "INSERT INTO debts (fullName,amount) VALUES (?, ?)", 
    (name, money))
    conn.commit()
    cur.close()
    conn.close()

class TkinterApp(tk.Tk):
    def __init__(self, *args, **kwargs):
         
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)
         
        # creating a container
        container = tk.Frame(self) 
        container.pack(side = "top", fill = "both", expand = True)
  
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
  
        # initializing frames to an empty array
        self.frames = {} 
        for F in (StartPage, Page1, Page2):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    pass
name_var=tk.StringVar()
money_var=tk.StringVar()
name_entry=tk.Entry(frame,textvariable=name_var)
name_label=tk.Label(frame, text="Nimi")
money_entry=tk.Entry(frame,textvariable=money_var)
money_label=tk.Label(frame, text="Summa")
sub_btn=tk.Button(frame,text = 'Submit', command = submit)

name_label.grid(row=0,column=0)
name_entry.grid(row=0,column=1)
money_label.grid(row=1,column=0)
money_entry.grid(row=1,column=1)
sub_btn.grid(row=2,column=1)

window.mainloop()
