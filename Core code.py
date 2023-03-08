# This is core code file 
# Scrapping  without API Create
 
from flask import Flask,render_template,redirect,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pymongo
import logging

# Setup MongoDB Data Base 
client = pymongo.MongoClient("mongodb+srv://AnantShah002:********@cluster0.0eigvos.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db=client["Product_Reviews_Scrapping"]
product_coll=db["Product_Name"]

# Create Flask
app=Flask(__name__)

@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")


# Create Screpting Links 
''' Varaiables'''

flipcart_home="https://www.flipkart.com"
flipcart_search="https://www.flipkart.com/search?q="
flipcart_search_product="iphone"
flipcart_search_product_link=flipcart_search+flipcart_search_product

''' Varaiables'''


# Start Now for Scuppting Data from Flipcat
flipcart_url=urlopen(flipcart_search_product_link).read() # Open url And Read File Like HTML
flipcart_bs=bs(flipcart_url,"html.parser")  # Beautify our flie to unders stand literibit
flipcart_product_list=flipcart_bs.find_all("div",{"class":"_1AtVbE col-12-12"}) # Now It's give me all product list data
#### flipcart_product_list has :- 30 product list 


# Now we start to select any one product Inside in this products list
''' check product list product is right.
If not then remove inside this product list''' 
products_list=[]
def product_filet(list_data):
    for i in range(len(list_data)):
        try:
            link=flipcart_home+list_data[i].div.div.div.a["href"]
            products_list.append(link)# Now this is generate product link
        except Exception as e:
            print(e)
            pass
        else:
            print(link)
            pass
    else:
        print(len(list_data))
        pass
product_filet(flipcart_product_list)

#### products_list has :- 24 right product for scruppting data
# print(len(products_list))

# Now we start proces for select one product and start scrupting that data
''' Select any one product & open product_url Converrt inot "html.parser" '''
product=products_list[0]  # Select which product I want to scruppting data
print(product)
product_link=requests.get(product) # <Response [200]> OR # Open url And Read File Like HTML
product_bs=bs(product_link.text,"html.parser") # Beautify our flie to unders stand literibit

# Now we try to scrupt product review data from
''' Start product review dat scruppting '''
product_data=product_bs.find_all("div",{"class":"_1AtVbE col-12-12"})
#### product data have:- 20 Type of data avelable 
## But we need only product review data
# (_16PBlm _3_IKGE):7 & (col _2wzgFH):10 data
product_review=product_bs.find_all("div",{"class":"col _2wzgFH"})
# print(len(product_review))
#### product review have 10 data

# Now we build a Function for Scrupting data 
review_data=[]
no=0
no_error=0
@app.route("/")
def data_scruppting(list_data=product_review):

    for i in range(len(list_data)):
        # print("For Loop")
        try:
            global no
            name = list_data[i].find("div",{"class":"row _3n8db9"}).div.p.text
            rattings = list_data[i].div.div.text
            head_line = list_data[i].div.p.text
            comment = list_data[i].find("div",{"class":""}).div.text
            details = [j.text for j in list_data[i].find("div",{"class":"row _3n8db9"}).div if j.text!=""]
            # Store my all data into dict fome
            no+=1
            data_dict={"No.":no,
                    "Name": name,
                    "Rattings⭐":rattings,
                    "Head Line": head_line,
                    "Comment":comment,
                    "Details":details}
            review_data.append(data_dict)
            print(data_dict)
        except Exception as e:
            global no_error
            no_error+=1
            print(f"{no_error}) {e}")

# data_scruppting(product_review)

# Now we are open all review page
all_review_data=product_bs.find("div",{"class":"col JOpGWq"})
all_review_data=all_review_data.find_all("a")
all_review_data=all_review_data[len(all_review_data)-1]["href"]

all_review_link=flipcart_home+all_review_data
# print(all_review_link)

# Now we are apen all The review text
all_reviws_link_req=requests.get(all_review_link)
all_reviws_link_bs=bs(all_reviws_link_req.text,"html.parser")
all_review_data_list=all_reviws_link_bs.find_all("div",{"class":"_1AtVbE col-12-12"})

# print(len(all_review_data_list))



# Crearte one more Finction for Scruppting Data Auttomaticly next page one by one 
_all_review_data=[]
_all_no=0
_all_no_next_page=1
_all_no_error=0
# @add.rou()
def data_scruppting1(list_data,All,time=3):
    global _all_no_next_page
    global _all_no_error
    for i in range(len(list_data)):
        try:
            global _all_no
            
            name = list_data[i].find("div",{"class":"row _3n8db9"}).div.p.text 
            rattings = list_data[i].div.div.div.div.div.text
            head_line = list_data[i].div.div.div.div.p.text
            comment = list_data[i].find("div",{"class":""}).div.text
            details = [j.text for j in list_data[i].find("div",{"class":"row _3n8db9"}).div if j.text!=""]
            # Store my all data into dict fome
            _all_no+=1
            data_dict={
                       "Page_No.":_all_no_next_page,"No.":_all_no,
                       "Name": name,
                    #    "Rattings⭐":rattings,
                       "Head Line": head_line,
                    #    "Comment":comment,
                       "Details":details}
            print(data_dict)
        except Exception as e:
            _all_no_error+=1
            print(f"{_all_no_error}) Error {e}")
            pass
        
        else:
            # print(data_dict)
            pass

    else:
        _all_no_next_page+=1
        try:
            link=list_data[len(list_data)-1].findAll("a",{"class":"_1LKTO3"})
            for j in link:
                if j.text=="Next":
                    next_page_link=flipcart_home+j["href"]
                    next_page_link_req=requests.get(next_page_link)
                    next_page_bs=bs(next_page_link_req.text,"html.parser")
                    next_page_reviews=next_page_bs.find_all("div",{"class":"_1AtVbE col-12-12"})
            
            print("\n")
            if All==True:
                print(next_page_link)
                data_scruppting1(next_page_reviews,True)
            elif All==False and _all_no_next_page<=time:
                print(next_page_link)
                data_scruppting1(next_page_reviews,False)
            else:
                pass
        except Exception as e:
            print(f"Re-Error⭐ {e}")

# data_scruppting1(all_review_data_list,False,10)

if __name__=="__main__":
    app.run(host="0.0.0.0")

