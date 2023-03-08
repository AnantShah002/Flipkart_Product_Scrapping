from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo 
import logging
import code
logging.basicConfig(filename="scrapper.log",level=logging.NOTSET,format="%(asctime)s %(name)s %(levelname)s %(message)s ")

logging.info("Start Implementing The Concept")

# Setup MongoDB Data Base 
client = pymongo.MongoClient("mongodb+srv://AnantShah002:AnantShah002@cluster0.0eigvos.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db=client["Product_Reviews_Scrapping"]
product_coll=db["Product_Name"]
logging.info("This is my MongoDB Data base directory " + str(product_coll) )


app = Flask(__name__)
logging.info("Flask API")


@app.route("/", methods = ['GET'])
def homepage():
    logging.warning("Clint is on Home Page")
    return render_template("index.html")

@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            # Collect clint Input data
            search = request.form['content'].replace(" ","")
            all_page=request.form.get("allpages")
            no_pages=request.form.get("no_pages")
            logging.info("client insert product related details")

            ### Apply Methord 
            # get clint serch link
            search_pro=code.serch(search)
            logging.info("Clint product search link:- " + str(search_pro) )
            # Serch prodects list in BeautifulSoup
            search_pro_bs=code.open_url_bs(search_pro,True,"div",{"class":"_1AtVbE col-12-12"}) #30 product avelable 
            logging.info("search related product list "+ str(len(search_pro_bs) ))
            
            # Now check How many are products 
            search_pro_list=[]
            for i in range(len(search_pro_bs)):
                logging.info("Check is It product or not " + str(i) )
                try:
                    data=search_pro_bs[i].div.div.div.a["href"]
                    search_pro_list.append(data)
                    logging.info("Yes It is Product")
                except:
                    logging.error("It is not Product")
                    pass
            logging.info("How many are products "+ str(len(search_pro_list)) )

            # select product link
            product=code.flipkart_home+search_pro_list[0]
            logging.warning("Now select produc link :-" + str(product) )

            ### Now find product All Review URL
            # prodects link into html with BeautifulSoup
            product_bs=code.open_url_bs(product,False)
            find_all_review=product_bs.find("div",{"class":"col JOpGWq"}).findAll("a")
            all_review_link=code.flipkart_home + find_all_review[len(find_all_review)-1]["href"]
            logging.warning("Product All Reviews link:- " + str(all_review_link) )

            # All review link into html with BeautifulSoup
            all_review_bs=code.open_url_bs(all_review_link,True,"div",{"class":"_1AtVbE col-12-12"})
            logging.warning("open and Check how many review list " + str(len(all_review_bs)) )

            # All Review Data List Insert for scrappiong
            logging.warning("Give Data According Clint Want")
            if all_page=="on":
                logging.info("client want all reviews data about product")
                data_review=code.data_scrapping(all_review_bs,True)
            
            elif all_page!="on":
                try:
                    if int(no_pages)>=1:
                        logging.info("client wants review data pages "+str(int(no_pages)))
                        data_review=code.data_scrapping(all_review_bs,False,int(no_pages))
                    else:
                        logging.info("client want 1 page reviews data about product")
                        data_review=code.data_scrapping(all_review_bs,False,1)
                
                except:
                    logging.info("client want 1 page reviews data about product")
                    data_review=code.data_scrapping(all_review_bs,None,1)

            logging.info("Product Reviews data list "+ str(len(data_review)) )

            # Create csv file 
            filename = search + ".csv"
            fw = open(filename, "w")
            headers = " No.page, No., Name , Ratings⭐, Heading , Comment , Details \n"
            fw.write(headers)

            # insert data in my MongoDb data base
            product_coll.insert_many(data_review)
            logging.info("Now Time to see data in Review Page")
            logging.shutdown()
            return render_template("result.html",reviews=data_review)

        except:
            logging.error("website is down try again late")
            return render_template("index.html")

    return render_template('results.html')

if __name__=="__main__":
    app.run(host="0.0.0.0")
