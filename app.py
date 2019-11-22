# Mars Mission App
# Import modules
import pymongo
from flask import Flask, render_template
from scrape_mars import scrape

# Flask set up
app = Flask(__name__)

# create a connection to mongoDB with the pymongo.MongoClient class
client = pymongo.MongoClient('mongodb://localhost:27017')
print(client)
@app.route('/')
def home_page():
    # load database into variable
    db = client.scrapedb

    # load collection (table) into a variable using the find command. Must convert to list
    mars_info = list(db.mars_data.find())

    ### html file must be in subfolder templates, must link variable in html file to the python file ###
    return render_template('index.html', mars = mars_info)


@app.route('/scrape')
def mars_web_scrape():   
    db = client.scrapedb

    #load collections into variable
    collections = db.mars_data

    # Create new document
    mars_data = scrape()
    # Add new document
    collections.insert_one(mars_data)
    return "You just scraped the latest mars data"


# Flask set up
if __name__ == '__main__':
    app.run(debug=True)