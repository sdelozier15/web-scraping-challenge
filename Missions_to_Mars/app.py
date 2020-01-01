from flask import Flask, render_template, redirect, url_for, jsonify
import pymongo
import scrape_mars

app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

#Flask app routes
@app.route("/")
def home():
    db = client.mars_db
    col = db.results
   
    mars = list(col.find())
    print(mars)
    mars = mars[0]

    return render_template("index.html", results = mars)

@app.route("/scrape")
def get_data():
    data = scrape_mars.scrape()
    
    db = client.mars_db
    db.results.drop()
    db.results.insert(data)

    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug = True)
