from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# connect mongodb with flask
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars"
mongo = PyMongo(app)

# Set route
@app.route('/')
def index():

    # pull data from mongodb
    data = mongo.db.mars_data.find_one()

    # send data to html template to generate websites
    return render_template("index.html", mars=data)

@app.route ('/scrape')
def scrape():
    
    # delete exsiting data
    mongo.db.mars_data.drop()
   
    # get scape data
    get_data = scrape_mars.scrape()

    # store data to mongodb
    mongo.db.mars_data.insert_one(get_data)
    
    # go back to the root
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
