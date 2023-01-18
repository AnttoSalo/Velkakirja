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
        for F in (StartPage, NewDebtPage, SummaryPage):

            frame = F(container, self)
            self.frames[F] = frame
  
            frame.grid(row = 0, column = 0, sticky ="nsew")
  
        self.show_frame(StartPage)
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # Create widgets for the start page
        label = tk.Label(self, text="This is the start page")
        label.pack()
        
        button1 = tk.Button(self, text="Uusi velka", 
                            command=lambda: controller.show_frame(NewDebtPage))
        button1.pack()
        
        button2 = tk.Button(self, text="Yhteenveto", 
                            command=lambda: controller.show_frame(SummaryPage))
        button2.pack() 

class NewDebtPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.money_var = tk.StringVar()

        first_name_label = tk.Label(self, text="Etunimi")
        first_name_label.grid(row=0,column=0)
        first_name_entry = tk.Entry(self, textvariable=self.first_name_var)
        first_name_entry.grid(row=0,column=1)
        
        last_name_label = tk.Label(self, text="Sukunimi")
        last_name_label.grid(row=1,column=0)
        last_name_entry = tk.Entry(self, textvariable=self.last_name_var)
        last_name_entry.grid(row=1,column=1)
        
        money_label = tk.Label(self, text="Summa")
        money_label.grid(row=2,column=0)
        money_entry = tk.Entry(self, textvariable=self.money_var)
        money_entry.grid(row=2,column=1)

        sub_btn = tk.Button(self, text = 'Submit', command = self.submit)
        sub_btn.grid(row=3,column=1)
        
    def submit(self):
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        money = self.money_var.get()

        cur.execute("INSERT INTO debts (first_name, last_name, amount) VALUES (?, ?, ?)", (first_name, last_name, money))
        conn.commit()

class SummaryPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        cur.execute("SELECT first_name, last_name, amount FROM debts")
        rows = cur.fetchall()
        for i, row in enumerate(rows):
            label_text = f"{row[0]} {row[1]}: {row[2]}"
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=0)
    

app = TkinterApp()  
app.geometry("800x600")  
app.mainloop()
cur.close()
conn.close()
