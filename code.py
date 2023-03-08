import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo 
import logging
import app

logging.basicConfig(filename="scrapper.log",level=logging.NOTSET,format="%(asctime)s %(name)s %(levelname)s %(message)s ")
logging.warning("This is code.py module file")

# Start frome there Flipkart Url
flipkart_home="https://www.flipkart.com"
# logging.info()

# Functune return clint search product link
def serch(search):
    flipkart_search="https://www.flipkart.com/search?q="
    clint_search=search #request.form['content'].replace(" ","")
    flipkart_search_product_link=flipkart_search+clint_search
    return flipkart_search_product_link

# Open Url. Read apply BeautifulSoup
def open_url_bs(link,alow,div="div",cls="c"):
    flipkart_url=requests.get(link)
    flipkart_url_bs=bs(flipkart_url.text,"html.parser")
    if alow==True:
        data_list=flipkart_url_bs.findAll(div,cls)
        return data_list
    else:
        return flipkart_url_bs

# Create Main Function For this Project 
# Scrapping All importent things in this finction
# And Store That Important Data
review_data=[]
no=0
no_error=0
next_pages=1
def data_scrapping(list_data,alow,times=3):
    global next_pages
    for i in range(len(list_data)):
        try:
            name=list_data[i].find("div",{"class":"row _3n8db9"}).div.p.text
            ratings = int(list_data[i].div.div.div.div.div.text)
            heading = list_data[i].div.div.div.div.p.text
            comment = list_data[i].find("div",{"class":""}).div.text
            details = [j.text for j in list_data[i].find("div",{"class":"row _3n8db9"}).div if j.text!=""]
            logging.info("Check is Product review")
            global no
            no+=1
            data_dict={"No.page":next_pages,"No.":no,
                       "Name":name,
                       "Ratings⭐":[ratings,ratings*"⭐"],
                       "Heading":heading,
                       "Comment":comment,
                       "Details":details
                           }
            review_data.append(data_dict)
            logging.info("Review data:- " +str(data_dict))
            
        except Exception as e:
            logging.error("Product Review Error:- "+str(e))
            pass
    else:
        next_pages+=1
        try:
            link=list_data[len(list_data)-1].findAll("a",{"class":"_1LKTO3"})
            for j in link:
                if j.text=="Next":
                    next_page_link=flipkart_home+j["href"]
                    logging.warning("Next Page Review Link:- "+str(next_page_link))
                    next_page_bs=open_url_bs(next_page_link,True,"div",{"class":"_1AtVbE col-12-12"})
                    logging.info("open Next Page Review with BeautifulSoup ")
                else:
                    pass

            if next_pages<=times and alow==None:
                logging.info("Re-call Function")
                data_scrapping(next_page_bs,None,times)

            elif next_pages<=times and alow==False:
                logging.info("Re-call Function")
                data_scrapping(next_page_bs,False,times)
            
            elif alow==True:
                logging.info("Re-call Function")
                data_scrapping(next_page_bs,True)
        except Exception as e:
            logging.error("Error:- " + str(e))
            return review_data
    logging.info("Every Thing Work ")
    logging.shutdown()
    return review_data
        

        
    