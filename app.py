# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 21:18:53 2021

@author: Viji
"""


# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape3_mars


# Flask Setup

app = Flask(__name__)


# PyMongo Connection Setup

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


# Flask Routes

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.mars
    mars_data = scrape3_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful"

# Define Main Behavior
if __name__ == "__main__":
    app.run()


