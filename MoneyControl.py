import json
import requests
from bs4 import BeautifulSoup

url1 = "http://www.moneycontrol.com/india/stockmarket/pricechartquote/"


json_array = []
management2 = []
industry_type = []
location = []
netsales=[]
netprofit=[]
name = []
def trade_spider(url):
        print(url)

        # below statement helps us to retrieve data of url
        source_code = requests.get(url)

        # just get the code, no headers or anything
        plain_text = source_code.text

        # BeautifulSoup objects can be sorted through easy
        # below, we made a BeautifulSoup object by passing the retrieved data/source_code as argument
        soup = BeautifulSoup(plain_text)
        # print(soup.prettify())
        # for tag in soup.find_all("tr",bgcolor="f6f6f6"):
        for tag in soup.find_all("a",class_="bl_12"):
            tag2 = tag.get('href')
            if tag2!="javascript:;":
                if tag2!="":
                    name.append(tag.get_text())
                    source_code = requests.get(tag2)
                    plain_text = source_code.text
                    soup = BeautifulSoup(plain_text)
                    manage(soup)
                    type_of_industry(soup)
                    net_sales(soup)
                    loc(soup)
                    net_profit(soup)
                    
# for location of the company
def loc(soup):

        for tag in soup.find_all("div" , class_="w252 FL"):
            tag2 = soup.findAll("div", class_="PT3 PB3 brdb")
            tag3=tag2[1].get_text()
            tag3=tag3.strip().replace("City","").strip()
            print(tag3)
            location.append(tag3)

# for information on the management of a company
def manage(soup):

        management=[]
        name=[]
        designation=[]

        for tag in soup.find_all("div",class_="w252 FR"):
            tag2 = tag.findAll("div",class_="FL w120 gD_13")
            for val in range(len(tag2)):
                if (val % 2 == 0): #even
                    name.append(tag2[val].get_text())
                else:
                    designation.append(tag2[val].get_text())
            for val in range(len(name)):
                management.append(name[val]+" : "+designation[val])
            management2.append(management)

# Type of company
def type_of_industry(soup):
        for tag in soup.find_all("a",class_="gry10"):
            industry_type.append(tag.get_text())

# some stats about companies
def net_sales(soup):
        for tag in soup.find_all("div",id="findet_1"):
            tag2 = tag.findAll("tr")
            tag3 = tag2[1].get_text()
            tag4 = tag3.replace("Net Sales","")
            tag5 = tag4.strip().replace(" ",", ")
            netsales.append(tag5)
            
# some other stats about companies
def net_profit(soup):
        for tag in soup.find_all("div",id="findet_1"):
            tag2 = tag.findAll("tr")
            tag3 = tag2[4].get_text()
            tag4 = tag3.replace("Net Profit","")
            tag5 = tag4.strip().replace(" ",", ")
            # print(tag5)
            netprofit.append(tag5)


array = ['A']
for val in array:
    trade_spider(url1+val)

number = len(industry_type)
for abc in range(number):
    json_array.append({
    "management":management2[abc],
    "industry_type":industry_type[abc],
    "net_sales":netsales[abc],
    "loc":location[abc],
    "net_profit":netprofit[abc],
    "company_name":name[abc]
})

with open("moneycontrol.json", "w") as outf:
    json.dump(json_array, outf)
