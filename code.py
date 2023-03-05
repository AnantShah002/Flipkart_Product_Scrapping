from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
import pymongo
import logging

# Setup MongoDB Data Base 
client = pymongo.MongoClient("mongodb+srv://AnantShah002:AnantShah002@cluster0.0eigvos.mongodb.net/?retryWrites=true&w=majority")
db = client.test
db=client["Product_Reviews_Scrapping"]
product_coll=db["Product_Name"]


# Create Flask
app=Flask(__name__)

# Home Page (Search Page)
@app.route("/", methods = ['GET'])
def homepage():
    return render_template("index.html")

# Create Pletfome Links for Web Scrupping

# Create Screpting Links 
''' Varaiables'''


@app.route("/review" , methods = ['POST' , 'GET'])
def index():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(" ","")
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            print(flipkart_url)
            return "<h1>flipkart_url<h1>"
        except :
            pass 
