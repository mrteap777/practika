import sqlite3
import ttkbootstrap as ttk
import tkinter as tk
from tkinter import *
import numpy as np
from pandastable import Table, TableModel
import pandas as pd
con = sqlite3.connect('bd (3) — копия — копия — копия.sqlite3')
f = pd.read_sql_query('select * from client',con=con)
df = pd.DataFrame(f)
df['status'] =pd.to_numeric (df['status'],errors='coerce').fillna(0).astype(int)
df.info()
cur=con.cursor()
cur.execute('BEGIN EXCLUSIVE')
# cur.execute('select * from client')
# client = cur.fetchall()
ip1=[]
date1=[]
stasta=[]
file = open("access_logs.log", "r")
for i in file:

    spisok=i.split(' ')
    ip=spisok[0]
    # print( ip)
    ip1.append(ip)
    date=spisok[3].replace("[","")
    date1.append(date)
    зона=spisok[4].replace("]","")
    строка_запроса=spisok[5]+spisok[6]+spisok[7]
    код_состояния=spisok[8]
    stasta.append(код_состояния)
    размер_объекта=spisok[9]
    ссылка=spisok[10]
    клиентский_браузер=spisok[11]


    cur.execute('''INSERT INTO LOGI( "ip", "date", "Зона ", "Строка запроса", "код_состояния", "размер объекта", "ссылка",
               "клиентский браузер") VALUES (?, ?,?,?,?,?,?,?)''', (ip,date,зона,строка_запроса,код_состояния,размер_объекта,ссылка,клиентский_браузер))
print(ip)
class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Мужской вход")
        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()
        self.window_width = 300
        self.window_height = 200
        self.x = (self.screen_width / 2) - (self.window_width / 2)
        self.y = (self.screen_height / 2) - (self.window_height / 2)
        self.master.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, self.x, self.y))



        self.login1 = ttk.Label(self.master, text='Введите мужицкий логин')
        self.login1.pack(pady=10)
        self.login1 = ttk.Entry(self.master)
        self.login1.pack()
        self.password1 = ttk.Label(self.master, text='Введите мужицкий пароль')
        self.password1.pack(pady=10)
        self.password1 = ttk.Entry(self.master)
        self.password1.pack()

        def proverka():
            login = str(self.login1.get())
            password = str(self.password1.get())
            try:
                self.vhod = cur.execute(
                    f'select id,login, password,status from client where login={login} and password={password} ').fetchall()
                if str(self.vhod[0][1]) == login and str(self.vhod[0][2]) == password:
                    print('Успешный вход')
                    self.open_window2()
                    self.master.withdraw()

            except:
                print('Неверные данные')

        btn = ttk.Button(self.master, text='Вход', command=proverka)
        btn.pack(pady=20)






    def open_window2(self):
        self.window2 = tk.Toplevel(self.master)
        self.window2.title("Данные логов")
        self.nbWin2 = ttk.Notebook(self.window2)
        self.tab1Win2 = ttk.Frame(self.nbWin2)
        self.nbWin2.add(self.tab1Win2, text='Данные логов')
        self.nbWin2.pack(expand=1, fill='both')
        unique_values5 =[]
        unique_values = pd.unique(ip1)
        for i in unique_values:
            unique_values1=i.replace("'", "")

            unique_values2=unique_values1.replace(" ","")

            unique_values5.append(unique_values2)

        self.kategoria = ttk.Combobox(self.tab1Win2, values=unique_values5)
        self.kategoria.pack(pady=10)

        unique_date5 = []
        unique_date = pd.unique(date1)
        for i in unique_date:
            unique_date1 = i.replace("'", "")

            unique_date2 = unique_date1.replace(" ", "")

            unique_date5.append(unique_date2)

        self.kategoria1 = ttk.Combobox(self.tab1Win2, values=unique_date5)
        self.kategoria1.pack(pady=10)

        sta5 = []
        sta = pd.unique(stasta)
        for i in sta:
            sta1 = i.replace("'", "")

            sta2 = sta1.replace(" ", "")

            sta5.append(sta2)

        self.kategoria11 = ttk.Combobox(self.tab1Win2, values=sta5)
        self.kategoria11.pack(pady=10)


        rez = cur.execute('select * from LOGI').fetchall()

        columns = ("id","ip","date","Зона ","Строка запроса","код_состояния","размер объекта","ссылка","клиентский браузер")

        self.tree = ttk.Treeview(self.tab1Win2, bootstyle="success", columns=columns, show='headings')
        self.tree.pack(pady=10)
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c,anchor=CENTER, minwidth=0, width=130)
        for value in rez:
            self.tree.insert('', END, values=value)
        def cat_vubor():
            if self.kategoria.get()=="":
                self.kat = "ip"
            else:
                self.kat=self.kategoria.get()
            if self.kategoria1.get()=="":
                self.kat1 = "date"
            else:
                self.kat1=self.kategoria1.get()
            if self.kategoria11.get()=="":
                self.kat11 = "код_состояния"
            else:
                self.kat11=self.kategoria11.get()

            rez = cur.execute(f'select * from LOGI where ip = "{self.kat}" and date="{self.kat1}" and код_состояния="{self.kat11}"').fetchall()


            columns = ("id", "ip", "date", "Зона ", "Строка запроса", "код_состояния", "размер объекта", "ссылка",
                       "клиентский браузер")
            self.tree.destroy()
            self.tree = ttk.Treeview(self.tab1Win2, bootstyle="success", columns=columns, show='headings')
            self.tree.pack(pady=10)
            for c in columns:
                self.tree.heading(c, text=c)
                self.tree.column(c,anchor=CENTER, minwidth=0, width=130)
            for value in rez:
                self.tree.insert('', END, values=value)

            self.btnctg.destroy()
            self.btnctg = ttk.Button(self.tab1Win2, text='Отсортировать', command=cat_vubor)
            self.btnctg.pack(pady=20)


        self.btnctg = ttk.Button(self.tab1Win2, text='Отсортировать', command=cat_vubor)
        self.btnctg.pack(pady=20)



    #


if __name__ == "__main__":
    root = tk.Tk()
    
    app = MainWindow(root)
    root.mainloop()