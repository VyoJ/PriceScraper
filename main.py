import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import re
import mysql.connector as sqltor
from datetime import datetime as dt
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


def onClickURL():
    '''
    Function to implement adding or removing URLs from the URL watchlists.
    '''

    w1 = Tk()
    w1.title('Edit URLs')
    w1.geometry('620x200')

    def onClickAdd():
        def AddURL():
            URL = entrybox1.get()
            entrybox1.setvar("Enter URL")
            if "amazon" in URL:
                uid = gen_UID("Amazon")
            elif "flipkart" in URL:
                uid = gen_UID("Flipkart")
            else:
                messagebox.showwarning("Warning", "Not an Amazon or Flipkart URL! Try again.")
                return
            try:
                curs.execute("INSERT INTO URLS VALUES('{}', '{}');".format(uid, URL))
            except:
                messagebox.showwarning("Warning", "URL entered is too long for the database. Use another one and try again!")
                w2.destroy()
            mydb.commit()
            curs.execute("SELECT URL FROM URLS WHERE URL = '{}';".format(URL))
            if URL in curs.fetchall()[0][0]:
                messagebox.showinfo("Success", "URL added to database successfully!")
            else:
                messagebox.showwarning("Warning", "Something went wrong! Try again later.")
            w2.destroy()

        w2 = Tk()
        w2.title("Add URLs")
        w2.geometry("600x150")
        entrybox1 = Entry(w2)
        entrybox1.place(relx = 0.015, rely = 0.2, width = 580)
        submit_btn = Button(w2, text = "Submit", font = ("Arial 14"), relief = RIDGE, bd = 3, command = AddURL)
        submit_btn.place(relx = 0.42, rely = 0.6)
        w2.mainloop() 

    def onClickDel():
        def DelURL():
            URL = entrybox2.get()
            entrybox2.setvar("Enter URL")
            curs.execute("SELECT URL FROM URLS WHERE URL = '{}';".format(URL))
            urls = list(map(lambda x: x[0], curs.fetchall()))
            if URL in urls:
                curs.execute("DELETE FROM URLS WHERE URL = '{}';".format(URL))
                mydb.commit()
                curs.execute("SELECT URL FROM URLS WHERE URL = '{}';".format(URL))
                if not(curs.fetchall()):
                    messagebox.showinfo("Success", "URL removed from database successfully!")
                else:
                    messagebox.showwarning("Warning", "URL could not be removed. Please try again later.")
            else:
                messagebox.showwarning("Warning", "This URL doesn't exist in the table.")
            w2.destroy()

        w2 = Tk()
        w2.title("Delete URLs")
        w2.geometry("600x200")
        entrybox2 = Entry(w2)
        entrybox2.place(relx = 0.015, rely = 0.2, width = 580)
        submit_btn = Button(w2, text = "Submit", font = ("Arial 14"), relief = RIDGE, bd = 3, command = DelURL)
        submit_btn.place(relx = 0.42, rely = 0.6)
        w2.mainloop()

    bt1 = Button(w1, text="Add URLs", font = ("Arial 12"), relief = RIDGE, bd = 3, command=onClickAdd)
    bt1.place(relx = 0.2, rely = 0.4)
    bt2 = Button(w1, text='Delete URLs', font = ("Arial 12"), relief = RIDGE, bd = 3, command=onClickDel)
    bt2.place(relx = 0.65, rely = 0.4)
    w1.mainloop()


def onClickVary():
    '''
    Function to show the Price variations of each product as a table.
    '''

    w2 = Tk()
    w2.title('Price Variations')
    w2.geometry("1280x500")

    style = ttk.Style(w2)
    style.theme_use('clam')

    curs.execute("SELECT DISTINCT Name FROM Products;")
    data = curs.fetchall()
    options = list(map(lambda x: x[0], data))
    menu = StringVar(w2)
    menu.set("Select Any Product")
    drop = OptionMenu(w2, menu, *options, command = lambda x: showTable(w2, menu.get()))
    drop.place(relx = 0.4, rely = 0.05)

    w2.mainloop()


def showTable(w2, name):
    '''
    Function to display the MySQL table storing products' names and prices along with the timestamp. 
    '''

    tree = ttk.Treeview(w2, column=("Timestamp", "Product Name", "Price"), show='headings', height=15)
    tree.column("#1", anchor=CENTER, width = 300)
    tree.heading("#1", text="Timestamp")
    tree.column("#2", anchor=CENTER, width = 500)
    tree.heading("#2", text="Product Name")
    tree.column("#3", anchor=CENTER, width = 400)
    tree.heading("#3", text="Price")
    curs.execute("SELECT Timestamp, Name, Price FROM Products WHERE Name = '{}' ORDER BY Timestamp;".format(name))
    data = curs.fetchall()
    for i in data:
        tree.insert('', 'end', text = "1", values = i)
    tree.place(relx = 0.03, rely = 0.2)


def gen_UID(website):
    '''
    Function to generate unique identification codes for all URLs being added to the table.
    '''

    curs.execute("SELECT DISTINCT UID FROM URLS WHERE UID REGEXP '[{}]$' ORDER BY UID DESC LIMIT 1;".format(website[0]))
    l_uid = curs.fetchall()
    if not(l_uid):
        uid = 'P1'+website[0]
    else:
        num = ""
        for i in l_uid[0][0]:
            if i.isdigit():
                num += i
        uid = 'P' + str(int(num)+1) + website[0]
    return uid


def get_amazon_name(dom):
    '''
    To get product names from Amazon URLs by inspecting the HTML.
    '''

    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        [name.strip() for name in name]
        return name[0]
    except Exception:
        return None


def get_amazon_price(dom):
    '''
    To get product prices from Amazon URLs by inspecting the HTML.
    '''

    try:
        price = dom.xpath('//span[@class="a-price-whole"]/text()')[0] #"a-offscreen"
        price = price.replace(',', '').replace('₹', '').replace('.00', '')
        return int(price)
    except Exception:
        return None


def get_flipkart_details(product_url):
    '''
    To get product names and prices from Flipkart URLs by inspecting the HTML.
    '''

    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    price_int = int(''.join(re.findall(r'\d+', price)))
    print(product_name + " is at " + price)
    curs.execute("SELECT UID FROM URLS WHERE URL = '{}'".format(product_url))
    uid = curs.fetchall()[0][0]
    curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {});".format(timestamp, uid, product_name, price_int))
    mydb.commit()


def mysqllogin():
    f = open("mysql_auth.txt", "a+")
    f.seek(0)
    data = f.read()
    if not(data):
        sqllogin = Tk()
        sqllogin.title("MySQL Login")
        sqllogin.geometry("400x300")
        username = StringVar()
        username.set("Enter MySQL username")
        pwd = StringVar()
        pwd.set("Enter MySQL password")
        userentry = Entry(sqllogin, textvariable = username)
        userentry.place(relx = 0.35, rely = 0.2)
        passentry = Entry(sqllogin, textvariable = pwd)
        passentry.place(relx = 0.35, rely = 0.5)
        submit_btn = Button(sqllogin, text = "Submit", font = ("Arial 14"), relief = RIDGE, bd = 3, command = lambda: f.writelines([userentry.get()+"\n", passentry.get()]) or sqllogin.destroy())
        submit_btn.place(relx = 0.42, rely = 0.8)
        sqllogin.mainloop()
    f.seek(0)
    details = f.readlines()
    f.close()
    return details


def GUI():
    '''
    Function to start the GUI of the program. 
    '''

    root = Tk()
    root.title('Home Page')
    root.geometry('1280x720')
    root.config(bg = "#FFFFFF")

    def graph(name, fig, canvas):
        plot1 = fig.add_subplot(111)
        curs.execute('SELECT UID FROM Products WHERE Name = "{}";'.format(name))
        data = curs.fetchall()
        uid = data[0][0]
        curs.execute("SELECT Timestamp, Price FROM products WHERE UID = '{}';".format(uid))
        res = curs.fetchall()
        x = [i[0] for i in res]
        y = [i[1] for i in res]
        plot1.scatter(x, y)
        canvas.draw()
        canvas.get_tk_widget().place(relx = 0.1, rely = 0.25)
        fig.delaxes(plot1)

    TLabel = Label(root, bg = "#000000", fg = "#ffe24b", anchor = "center", text = "Welcome to Price Tracker", font = ("Arial 20 bold"), padx = 5, pady = 5, relief = SUNKEN, bd = 5)
    TLabel.place(relx = 0.35, rely = 0.05)

    bt1 = Button(root, text="Edit URLs", font = ("Arial 14"), relief = RIDGE, bd = 3, command=onClickURL)
    bt1.place(relx = 0.17, rely = 0.17)
    bt2 = Button(root, text='View Price Variations', font = ("Arial 14"), relief = RIDGE, bd = 3, command=onClickVary)
    bt2.place(relx = 0.7, rely = 0.17)

    fig = Figure(figsize=(10, 5), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=root)
    curs.execute("SELECT DISTINCT Name FROM Products;")
    data = curs.fetchall()
    options = list(map(lambda x: x[0], data))

    menu = StringVar(root)
    menu.set("Select Any Product")
    drop = OptionMenu(root, menu, *options, command = lambda x: graph(menu.get(), fig, canvas))
    drop.place(relx = 0.4, rely = 0.2)
    
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    root.mainloop()


#main
while True:
    details = mysqllogin()
    try:
        mydb = sqltor.connect(host="localhost", user=details[0].strip(), passwd=details[1].strip())
    except:
        with open("mysql_auth.txt", "w") as f:
            pass
        continue
    break
    
curs = mydb.cursor()
if mydb.is_connected():
    print("Connected")

curs.execute("CREATE DATABASE IF NOT EXISTS PRICETRACKER;")
curs.execute("USE PRICETRACKER;")
curs.execute("SHOW TABLES;")
data = curs.fetchall()

if not(data) or not(data[1][0]):
    curs.execute('''CREATE TABLE URLS(
    UID CHAR(6),
    URL VARCHAR(400));''')
    onClickURL()
    
if not(data) or not(data[0][0]):
    curs.execute('''CREATE TABLE PRODUCTS(
    Timestamp DATETIME,
    UID CHAR(6),
    Name VARCHAR(200),
    Price INT);''')

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

curs.execute("SELECT URL FROM URLS WHERE UID LIKE '%A';")
data = curs.fetchall()
amazon_urls = list(map(lambda x: x[0], data))
print(amazon_urls)

for product_url in amazon_urls:
    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))
    
    price = get_amazon_price(main_dom)
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    if not(price):
        messagebox.showwarning("Warning", "URL could not be reached right now. Please try again later.")
        break
    product_name = get_amazon_name(main_dom).strip()
    print(product_name, price)
    curs.execute("SELECT UID FROM URLS WHERE URL = '{}'".format(product_url))
    uid = curs.fetchall()[0][0]
    curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {});".format(timestamp, uid, product_name, price))
    mydb.commit()

curs.execute("SELECT URL FROM URLS WHERE UID LIKE '%F';")
data = curs.fetchall()
flipkart_urls = list(map(lambda x: x[0], data))
print(flipkart_urls)

for product_url in flipkart_urls:
    get_flipkart_details(product_url)

GUI()

mydb.close()