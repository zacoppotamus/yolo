import urllib2
import json

url = "http://search.twitter.com/search.json?q=yolo&rpp=50&include_entities=true&with_twitter_user_id=true&result_type=mixed"

url2 = "http://api.semetric.com/sentiment?token=2a4277ac1ae94261aabce70284506e1f&text="


if __name__ == "__main__":
    tweets = json.loads(urllib2.urlopen(url).read())
    sentiments = [0]*5
    for tweet in tweets["results"]:
        text = tweet["text"]
        q = urllib2.quote(text.encode("utf-8"))
        result = urllib2.urlopen(url2+q).read()
        p = json.loads(result)
        print p["response"][0]["score"]
        sentiments[p["response"][0]["score"]-1] += 1
    print sentiments

