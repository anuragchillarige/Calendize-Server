import os
from flask import Flask, request, render_template, jsonify
import Utilities
import json
import FirebaseUtilities

# Edit this One AI API call using our studio at https://studio.oneai.com/?pipeline=1IhlEE&share=true


app = Flask(__name__)
link = {}

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
        data.append(Utilities.get_rss_news_data(links[i]))
    response = jsonify(data)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@ app.route('/')
def home():
    return render_template('index.html')


@ app.route("/test")
def test():
    return "testing!"



if __name__ == '__main__':
    app.run()
