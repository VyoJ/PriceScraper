import requests
from bs4 import BeautifulSoup
from lxml import etree as et
import re
import matplotlib.pyplot as plt
import numpy as np
import schedule as sch
import time as tm

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
    'Accept': '*/*', 
    'Accept-Encoding': 'gzip, deflate, br', 
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
}

amazon_urls = ['https://www.amazon.in/Apple-iPhone-128GB-Product-RED/dp/B0BDJVSDMY/ref=sr_1_3?keywords=iphone%2B14&qid=1671965973&sprefix=iph%2Caps%2C303&sr=8-3&th=1',
"https://www.amazon.in/Xbox-Series-X/dp/B08J7QX1N1"]

flipkart_urls = ["https://www.flipkart.com/apple-iphone-14-midnight-128-gb/p/itm9e6293c322a84?pid=MOBGHWFHECFVMDCX&lid=LSTMOBGHWFHECFVMDCXBOYSND&marketplace=FLIPKART&q=iphone+14&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=1c136774-01a9-46d3-a2e3-788f967e8061.MOBGHWFHECFVMDCX.SEARCH&ppt=hp&ppn=homepage&ssid=myp3m3u1w6cdawhs1671967395943&qH=860f3715b8db08cd",
"https://www.flipkart.com/apple-iphone-13-green-128-gb/p/itm18a55937b2607?pid=MOBGC9VGSU9DWGJZ&lid=LSTMOBGC9VGSU9DWGJZTOZYKQ&marketplace=FLIPKART&q=iphone+13&store=tyy%2F4io&srno=s_1_1&otracker=search&otracker1=search&fm=Search&iid=3a1a1c47-12b2-4664-abd3-979acf56983e.MOBGC9VGSU9DWGJZ.SEARCH&ppt=sp&ppn=sp&ssid=58bph5yzb1r1mubk1671967811312&qH=c68a3b83214bb235"]

def get_amazon_name(dom):
    try:
        name = dom.xpath('//span[@id="productTitle"]/text()')
        [name.strip() for name in name]
        return name[0]
    except Exception as e:
        name = 'Not Available'
        return None

def get_amazon_price(dom):
    try:
        price = dom.xpath('//span[@class="a-offscreen"]/text()')[0]
        price = price.replace(',', '').replace('₹', '').replace('.00', '')
        return int(price)
    except Exception:
        price = 'Not Available'
        return None

def update_prices(price_int):
    xpoints.append(1)
    ypoints.append(price_int)

for product_url in amazon_urls:
    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))

    price = get_amazon_price(main_dom)
    product_name = get_amazon_name(main_dom).strip()
    print(product_name, price)

for product_url in flipkart_urls:
    response = requests.get(product_url, headers=header)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_dom = et.HTML(str(soup))

    product_name = soup.find("span",{"class":"B_NuCI"}).get_text()
    price = soup.find("div",{"class":"_30jeq3 _16Jk6d"}).get_text()
    price_int = int(''.join(re.findall(r'\d+', price)))
    print(product_name + " is at " + price)
    
xpoints = []
ypoints = []

sch.every(1439).minutes.do(update_prices)
while True:
    sch.run_pending()
    tm.sleep(1)



# # importing libraries
# from bs4 import BeautifulSoup
# import requests
# import re

# def main(URL):
#     # opening our output file in append mode
#     File = open("out.csv", "a")

#     HEADERS = ({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
# 'Accept-Language': 'en-US, en;q=0.5'})

#     # Making the HTTP Request
#     webpage = requests.get(URL, headers=HEADERS)

#     # Creating the Soup Object containing all data
#     soup = BeautifulSoup(webpage.content, "lxml")

#     # retrieving product title
#     try:
#         # Outer Tag Object
#         title = soup.find("span", attrs={"id": 'productTitle'})

#         # Inner NavigableString Object
#         title_value = title.string

#         # Title as a string value
#         title_string = title_value.strip().replace(',', '')

#     except AttributeError:
#         title_string = "NA"
#     print("product Title = ", title_string)

#     # saving the title in the file
#     File.write(f"{title_string},")

#     # retrieving price
#     try:
#         price = soup.find('div', {"class": "a-price-whole"}, True)
#         # price = re.sub("[^0-9]", "", price)
#     except AttributeError:
#         price = "NA"
#     print("Products price = ", price)

#     File.write(f"{price},")

# #     # retrieving product rating
# #     try:
# #         rating = soup.find("i", attrs={
# #                            'class': 'a-icon a-icon-star a-star-4-5'})
# #                                     .string.strip().replace(',', '')
# #  
# #     except AttributeError:
# #  
# #         try:
# #             rating = soup.find(
# #                 "span", attrs={'class': 'a-icon-alt'})
# #                                 .string.strip().replace(',', '')
# #         except:
# #             rating = "NA"
# #     print("Overall rating = ", rating)
# #  
# #     File.write(f"{rating},")
# #  
# #     try:
# #         review_count = soup.find(
# #             "span", attrs={'id': 'acrCustomerReviewText'})
# #                                 .string.strip().replace(',', '')
# #  
# #     except AttributeError:
# #         review_count = "NA"
# #     print("Total reviews = ", review_count)
# #     File.write(f"{review_count},")
# #  
# #     # print availablility status
# #     try:
# #         available = soup.find("div", attrs={'id': 'availability'})
# #         available = available.find("span")
# #                     .string.strip().replace(',', '')
# #  
# #     except AttributeError:
# #         available = "NA"
# #     print("Availability = ", available)
# #  
# #     # saving the availability and closing the line
# #     File.write(f"{available},\n")
# #  
#     # closing the file
#     File.close()


# if __name__ == '__main__':
#     # opening our url file to access URLs
#     file = open("url.txt", "r")

#     # iterating over the urls
#     for links in file.readlines():
#         main(links)