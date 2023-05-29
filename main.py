import mysql.connector
import tkinter as tk
from tkinter import ttk, messagebox

dBase = mysql.connector.connect(
    host ='localhost3306',
    user ='root',
    passwd = 'marvel'
)

cursor = dBase.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS marvel")
cursor.close()
connect = mysql.connector.connect(
    host ='localhost3306',
    user ='root',
    passwd = 'marvel',
    database = 'marvel'
)
cursor2 = connect.cursor()
cursor2.execute('''CREATE TABLE IF NOT EXISTS MarvelInfo(
                            ID int(3) NOT NULL,
                            Movie varchar(80) NOT NULL,
                            DateInfo varchar(50) NOT NULL,
                            Mcu_Phase varchar(50)
                        )''')
idHolder = list()
holder = dict()
with open("Marvel.txt", 'r') as file:
    for l in file:
        l = l.strip()
        if l:
            movieInf = l.split()
            movieId = int(movieInf[0])
            movieName = movieInf[1]
            dateTime = movieInf[2]
            mcuPhase = movieInf[3]
            idHolder.append(movieId)
            holder[movieId]=movieName
            mySql_insert = """INSERT INTO MarvelInfo (ID,Movie,DateInfo,Mcu_Phase)
                                                      VALUES (%s,%s,%s,%s)"""
            value = (movieId, movieName, dateTime, mcuPhase)

            cursor2.execute(mySql_insert, value)

connect.commit()
def update(*args):
    Item= ddVar.get()
    for k in holder.keys():
        if Item == 'ID':
            textBox.delete(0, tk.END)
            break
        if int(k) == int(Item):
            textBox.delete(0, tk.END)
            textBox.insert(tk.END, holder[k])
            break
def addDb(idEntry, movieEntry, dateEntry, phaseEntry):
    idValue = idEntry.get()
    movieValue = movieEntry.get()
    dateValue = dateEntry.get()
    phaseValue = phaseEntry.get()
    with open("Marvel.txt", 'a') as file:
        file.write("\n"+idValue+" "+movieValue+" "+dateValue+" "+phaseValue)
    mySql_insert = """INSERT INTO MarvelInfo (ID,Movie,DateInfo,Mcu_Phase)
                                                          VALUES (%s,%s,%s,%s)"""
    values = (idValue, movieValue, dateValue, phaseValue)
    cursor2.execute(mySql_insert, values)
    connect.commit()
    if idValue and movieValue and dateValue and phaseValue:
        messagebox.showinfo("Data added to the database!")
    else:
        messagebox.showwarning("Please fill in all fields!")

def popup():
    popup_box = tk.Toplevel(window)
    popup_box.title("Data")
    popup_box.geometry("300x300")
    idLabel = tk.Label(popup_box, text="ID:")
    idLabel.pack()
    idEntry = tk.Entry(popup_box)
    idEntry.pack()
    movieLabel = tk.Label(popup_box, text="Movie:")
    movieLabel.pack()
    movieEntry = tk.Entry(popup_box)
    movieEntry.pack()
    dateLabel = tk.Label(popup_box, text="Date:")
    dateLabel.pack()
    dateEntry = tk.Entry(popup_box)
    dateEntry.pack()
    phaseLabel = tk.Label(popup_box, text="MCU Phase:")
    phaseLabel.pack()
    phaseEntry = tk.Entry(popup_box)
    phaseEntry.pack()
    okButton = tk.Button(popup_box, text="Ok", command=lambda: addDb(idEntry, movieEntry, dateEntry, phaseEntry))
    okButton.pack(side=tk.LEFT, padx=10)
    cancelButton = tk.Button(popup_box, text="Cancel", command=popup_box.destroy)
    cancelButton.pack(side=tk.RIGHT, padx=10)

def listData():
    cursor2.execute("SELECT * FROM MarvelInfo")
    result=cursor2.fetchall()
    listWindow = tk.Toplevel()
    listWindow.title("All Data")
    textBox = tk.Text(listWindow, width=30, height=30)
    textBox.pack()
    for r in result:
        textBox.insert(tk.END, f"ID: {r[0]}\n")
        textBox.insert(tk.END, f"Movie: {r[1]}\n")
        textBox.insert(tk.END, f"Date: {r[2]}\n")
        textBox.insert(tk.END, f"MCU Phase: {r[3]}\n")
        textBox.insert(tk.END, "\n")

window = tk.Tk()
window.title('Marvel Universe')

boxFrame = ttk.Frame(window, padding="20")
boxFrame.grid(row=0, column=0)
button1 = ttk.Button(boxFrame, text="Add", command=popup)
button1.grid(row=0, column=0, padx=5, pady=5)
button2 = ttk.Button(boxFrame, text="List All", command=listData)
button2.grid(row=0, column=1)
textBox = ttk.Entry(boxFrame, width=30)
textBox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

ddVar = tk.StringVar()
ddVar.trace('w', update)
dd = ttk.Combobox(boxFrame, textvariable=ddVar)
dd['values'] = ["ID"] + [i for i in range(1, idHolder[-1] + 1)]
dd.current(0)
dd.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

window.mainloop()
connect.close()
cursor2.close()