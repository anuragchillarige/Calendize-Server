import os
from flask import Flask, request, render_template, jsonify
import Utilities
import json
import FirebaseUtilities

# Edit this One AI API call using our studio at https://studio.oneai.com/?pipeline=1IhlEE&share=true


app = Flask(__name__)
UPLOADFOLDER = os.path.join(os.getcwd(), './icsFiles')
app.config['UPLOADFOLDER'] = UPLOADFOLDER
addedFile = False
link = []


@app.route("/rssFeed")
def rssFeed(link="http://rss.cnn.com/rss/cnn_world.rss"):
    feed = json.dumps(Utilities.get_rss_news_data(link), indent=4)
    print(feed)
    return feed


@app.route('/getLink', methods=["POST"])
def getLink():
    output = json.loads(request.data)
    link.append(output["link"])
    return output


@app.route('/addCalendar', methods=["POST"])
def addCalendar():
    output = json.loads(request.data)
    out = FirebaseUtilities.addCalendars(output['user'])
    return out


@app.route('/readRssLinks', methods=["POST", "GET"])
def readRssLinks():
    output = json.loads(request.data)
    links = FirebaseUtilities.readRssLinks(output['user'])
    data = []
    for i in links:
        data.append(Utilities.get_rss_news_data(i))
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    print(response)
    return response


@ app.route('/')
def home():
    return render_template('index.html')


@ app.route("/test")
def test():
    return "testing!"
