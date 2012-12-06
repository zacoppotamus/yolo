from flask import Flask, request, url_for
import json
import os
import urllib2
from random import choice
app = Flask(__name__)

url = "http://search.twitter.com/search.json?q=yolo&rpp=50&include_entities=true&with_twitter_user_id=true&result_type=mixed"

url2 = "http://api.semetric.com/sentiment?token=2a4277ac1ae94261aabce70284506e1f&text="

@app.route("/")
def index():
    return open("templates/index.html").read()


@app.route("/yolo")
def yolo():
    tweets = json.loads(urllib2.urlopen(url).read())
    result = choice(tweets["results"])
    text = result["text"]
    author = result["from_user"]
    madness_json = urllib2.urlopen(url2+urllib2.quote(text.encode("utf-8"))).read()
    p = json.loads(madness_json)
    madness = 5-p["response"][0]["score"] + 1

    return json.dumps({"madness":madness, "text":text, "author":author})

if __name__ == "__main__":
    app.debug = True
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
