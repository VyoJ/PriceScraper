# import requests
# from bs4 import BeautifulSoup
# from lxml import etree as et
# import re
# import mysql.connector as sqltor
# import matplotlib.pyplot as plt
# import numpy as np
# import schedule as sch
# from datetime import datetime as dt

# def get_amazon_name(dom):
#     '''
#     To get product names from Amazon URLs by inspecting the HTML.
#     '''

#     try:
#         name = dom.xpath('//span[@id="productTitle"]/text()')
#         [name.strip() for name in name]
#         return name[0]
#     except Exception:
#         name = 'Not Available'
#         return None

# def get_amazon_price(dom):
#     '''
#     To get product prices from Amazon URLs by inspecting the HTML.
#     '''

#     try:
#         price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
#         price = price.replace(',', '').replace('₹', '').replace('.00', '')
#         return int(price)
#     except Exception:
#         price = 'Not Available'
#         return None

# # def update_prices(price_int):
# #     '''
# #     To update prices every 12 hours from each of the websites for the specified URLs.
# #     '''

# #     xpoints.append(1)
# #     ypoints.append(price_int)

# def update_urls():
#     '''
#     Function to implement adding or removing URLs from the URL watchlists.
#     Will be updated to work through Tkinter.
#     '''

#     # print('''Do you want to enter another URL:
#     # 1. Amazon
#     # 2. Flipkart\n''')
#     # choice = int(input("Enter number corresponding to choice: "))
#     # if choice in (1,2):
#     #     url = input("Enter URL:")
#     #     if choice == 1:
#     #         amazon_urls.append(url)
#     #     elif choice == 2:
#     #         flipkart_urls.append(url)

# #main
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
#     'Accept': '*/*', 
#     'Accept-Encoding': 'gzip, deflate, br', 
#     'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
# }

# #main
# mydb = sqltor.connect(host="localhost", user="root", passwd="Root@604")
# curs = mydb.cursor()
# if mydb.is_connected():
#     print("Connected")

# curs.execute("CREATE DATABASE IF NOT EXISTS PRICE_TRACKER;")
# curs.execute("USE PRICE_TRACKER;")
# curs.execute("SHOW TABLES;")
# data = curs.fetchall()
# print(data)
# if not(data) or 'products' not in data[0][0]:
#     curs.execute('''CREATE TABLE PRODUCTS(
#     Timestamp DATETIME,
#     Website CHAR(10),
#     Name CHAR(50),
#     Price INT);''')

# amazon_urls = ['https://www.amazon.in/Apple-iPhone-128GB-Product-RED/dp/B0BDJVSDMY/ref=sr_1_3?keywords=iphone%2B14&qid=1671965973&sprefix=iph%2Caps%2C303&sr=8-3&th=1',
# "https://www.amazon.in/Xbox-Series-X/dp/B08J7QX1N1"]

# flipkart_urls = ["https://www.flipkart.com/apple-iphone-14-midnight-128-gb/p/itm9e6293c322a84?pid=MOBGHWFHECFVMDCX&lid=LSTMOBGHWFHECFVMDCXBOYSND&marketplace=FLIPKART&q=iphone+14&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=1c136774-01a9-46d3-a2e3-788f967e8061.MOBGHWFHECFVMDCX.SEARCH&ppt=hp&ppn=homepage&ssid=myp3m3u1w6cdawhs1671967395943&qH=860f3715b8db08cd",
# "https://www.flipkart.com/apple-iphone-13-green-128-gb/p/itm18a55937b2607?pid=MOBGC9VGSU9DWGJZ&lid=LSTMOBGC9VGSU9DWGJZTOZYKQ&marketplace=FLIPKART&q=iphone+13&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=3a1a1c47-12b2-4664-abd3-979acf56983e.MOBGC9VGSU9DWGJZ.SEARCH&ppt=sp&ppn=sp&ssid=58bph5yzb1r1mubk1671967811312&qH=c68a3b83214bb235"]

# # For plotting Matplotlib graphs
# # xpoints = []
# # ypoints = []

# for product_url in amazon_urls:
#     response = requests.get(product_url, headers=header)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     main_dom = et.HTML(str(soup))
    
#     price = get_amazon_price(main_dom)
#     timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
#     product_name = get_amazon_name(main_dom).strip()
#     print(product_name, price)
#     curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {})".format(timestamp, "Amazon", product_name, price))
#     mydb.commit()

# for product_url in flipkart_urls:
#     response = requests.get(product_url, headers=header)
#     soup = BeautifulSoup(response.content, 'html.parser')
#     main_dom = et.HTML(str(soup))

#     product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
#     price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
#     timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
#     price_int = int(''.join(re.findall(r'\d+', price)))
#     print(product_name + " is at " + price)
#     curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {})".format(timestamp, "Flipkart", product_name, price_int))
#     mydb.commit()

# # # Scheduling the program to run once every 12 hours:
# # sch.every(12).hours.do(lambda: print("Test"))
# # while True:
# #     sch.run_pending()
# #     tm.sleep(1)

# mydb.close()

import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import re
import mysql.connector as sqltor
from datetime import datetime as dt
from tkinter import *
from tkinter import messagebox
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
            entrybox1.setvar("")
            if "amazon" in URL:
                uid = gen_UID("Amazon")
            elif "flipkart" in URL:
                uid = gen_UID("Flipkart")
            else:
                messagebox.showwarning("Warning", "Not an Amazon or Flipkart URL! Try again.")
                return
            curs.execute("INSERT INTO URLS VALUES('{}', '{}');".format(uid, URL))
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
            entrybox2.setvar("")
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
    w2 = Tk()
    w2.title('Price Variations')
    w2.geometry('620x480') 
    w2.mainloop()


def gen_UID(website):
    curs.execute("SELECT DISTINCT UID FROM URLS WHERE UID REGEXP '[{}]$' ORDER BY UID DESC LIMIT 1;".format(website[0]))
    l_uid = curs.fetchall()
    if not(l_uid):
        uid = 'P001'+website[0]
    else:
        uid = 'P00' + str(int(str(l_uid[0][0])[1:4])+1) + website[0]
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
        name = 'Not Available'
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
        price = 'Not Available'
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


def GUI():
    root = Tk()
    root.title('Home Page')
    root.geometry('1280x720')
    root.config(bg = "#FFFFFF")

    TLabel = Label(root, bg = "#000000", fg = "#ffe24b", anchor = "center", text = "Welcome to Price Tracker", font = ("Arial 20 bold"), padx = 5, pady = 5, relief = SUNKEN, bd = 5)
    TLabel.place(relx = 0.35, rely = 0.05)

    bt1 = Button(root, text="Edit URLs", font = ("Arial 14"), relief = RIDGE, bd = 3, command=onClickURL)
    bt1.place(relx = 0.17, rely = 0.17)
    bt2 = Button(root, text='View Price Variations', font = ("Arial 14"), relief = RIDGE, bd = 3, command=onClickVary)
    bt2.place(relx = 0.7, rely = 0.17)

    fig = Figure(figsize=(5, 5), dpi=100)
    y = [i**2 for i in range(101)]
    plot1 = fig.add_subplot(111)
    plot1.plot(y)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(relx = 0.3, rely = 0.25)
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    root.mainloop()


#main
mydb = sqltor.connect(host="localhost", user="root", passwd="Root@604")
curs = mydb.cursor()
if mydb.is_connected():
    print("Connected")

curs.execute("CREATE DATABASE IF NOT EXISTS PRICETRACKER;")
curs.execute("USE PRICETRACKER;")
curs.execute("SHOW TABLES;")
data = curs.fetchall()
print(data)

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
    #FOREIGN KEY (UID) REFERENCES URLS(UID)

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
    product_name = get_amazon_name(main_dom).strip()
    print(product_name, price)
    curs.execute("SELECT UID FROM URLS WHERE URL = '{}'".format(product_url))
    uid = curs.fetchall()[0][0]
    curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {});".format(timestamp, uid, product_name, price))
    # else:
    #     uid = gen_UID("Amazon")
    #     curs.execute("INSERT INTO URLS VALUES ('{}','{}');".format(uid, product_url))
    #     curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {});".format(timestamp, uid, product_name, price))
    mydb.commit()

curs.execute("SELECT URL FROM URLS WHERE UID LIKE '%F';")
data = curs.fetchall()
flipkart_urls = list(map(lambda x: x[0], data))
print(flipkart_urls)

for product_url in flipkart_urls:
    get_flipkart_details(product_url)

GUI()

mydb.close()