import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import re
import mysql.connector as sqltor
import matplotlib.pyplot as plt
import numpy as np
import schedule as sch
from datetime import datetime as dt

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
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        price = price.replace(',', '').replace('₹', '').replace('.00', '')
        return int(price)
    except Exception:
        price = 'Not Available'
        return None

# def update_prices(price_int):
#     '''
#     To update prices every 12 hours from each of the websites for the specified URLs.
#     '''

#     xpoints.append(1)
#     ypoints.append(price_int)

def update_urls():
    '''
    Function to implement adding or removing URLs from the URL watchlists.
    Will be updated to work through Tkinter.
    '''

    # print('''Do you want to enter another URL:
    # 1. Amazon
    # 2. Flipkart\n''')
    # choice = int(input("Enter number corresponding to choice: "))
    # if choice in (1,2):
    #     url = input("Enter URL:")
    #     if choice == 1:
    #         amazon_urls.append(url)
    #     elif choice == 2:
    #         flipkart_urls.append(url)

#main
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

#main
mydb = sqltor.connect(host="localhost", user="root", passwd="Root@604")
curs = mydb.cursor()
if mydb.is_connected():
    print("Connected")

curs.execute("CREATE DATABASE IF NOT EXISTS PRICE_TRACKER;")
curs.execute("USE PRICE_TRACKER;")
curs.execute("SHOW TABLES;")
data = curs.fetchall()
print(data)
if not(data) or 'products' not in data[0][0]:
    curs.execute('''CREATE TABLE PRODUCTS(
    Timestamp DATETIME,
    Website CHAR(10),
    Name CHAR(50),
    Price INT);''')

amazon_urls = ['https://www.amazon.in/Apple-iPhone-128GB-Product-RED/dp/B0BDJVSDMY/ref=sr_1_3?keywords=iphone%2B14&qid=1671965973&sprefix=iph%2Caps%2C303&sr=8-3&th=1',
"https://www.amazon.in/Xbox-Series-X/dp/B08J7QX1N1"]

flipkart_urls = ["https://www.flipkart.com/apple-iphone-14-midnight-128-gb/p/itm9e6293c322a84?pid=MOBGHWFHECFVMDCX&lid=LSTMOBGHWFHECFVMDCXBOYSND&marketplace=FLIPKART&q=iphone+14&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=1c136774-01a9-46d3-a2e3-788f967e8061.MOBGHWFHECFVMDCX.SEARCH&ppt=hp&ppn=homepage&ssid=myp3m3u1w6cdawhs1671967395943&qH=860f3715b8db08cd",
"https://www.flipkart.com/apple-iphone-13-green-128-gb/p/itm18a55937b2607?pid=MOBGC9VGSU9DWGJZ&lid=LSTMOBGC9VGSU9DWGJZTOZYKQ&marketplace=FLIPKART&q=iphone+13&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=3a1a1c47-12b2-4664-abd3-979acf56983e.MOBGC9VGSU9DWGJZ.SEARCH&ppt=sp&ppn=sp&ssid=58bph5yzb1r1mubk1671967811312&qH=c68a3b83214bb235"]

# For plotting Matplotlib graphs
# xpoints = []
# ypoints = []

for product_url in amazon_urls:
    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))
    
    price = get_amazon_price(main_dom)
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    product_name = get_amazon_name(main_dom).strip()
    print(product_name, price)
    curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {})".format(timestamp, "Amazon", product_name, price))
    mydb.commit()

for product_url in flipkart_urls:
    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))

    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
    price_int = int(''.join(re.findall(r'\d+', price)))
    print(product_name + " is at " + price)
    curs.execute("INSERT INTO Products VALUES ('{}', '{}', '{}', {})".format(timestamp, "Flipkart", product_name, price_int))
    mydb.commit()

# # Scheduling the program to run once every 12 hours:
# sch.every(12).hours.do(lambda: print("Test"))
# while True:
#     sch.run_pending()
#     tm.sleep(1)

mydb.close()