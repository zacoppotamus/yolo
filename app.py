#!usr/bin/env

# This script parses the weather info from
# random coordinates reverse-geocodes them
# and changes the background color depending
# on the current temperature.

import json
import time
import os
from random import choice
from flask import Flask, session
from urllib2 import urlopen
from geopy import geocoders

app = Flask(__name__)

#forecast_key = Forecast.io API key

min_latitude = -90
max_latitude = 90
min_longtitude = -180
max_longtitude = 180

geo = geocoders.GoogleV3()

# Parse city coordinates from text file
f = open("unprocessed.txt")
f = f.readlines()
coord_list = []
for item in f:
	coord_list.append(item.replace("\n",""))

@app.route("/")
def index():
	return open("templates/index.html").read()

@app.route("/info")
def info():
	time.sleep(1)
	coordinates = choice(coord_list)
	(place, point) = geo.geocode(coordinates)

	latitude = str(coordinates.split(",")[0])
	longtitude = (str(coordinates.split(",")[1])).replace(" ","")
	url = "https://api.forecast.io/forecast/{0}/{1},{2}?units=si".format(forecast_key,latitude, longtitude)

	response = urlopen(url).read()

	obj = json.loads(response)
	current_summary = obj['hourly']['data'][0]['summary']
	daily_summary = obj['daily']['data'][0]['summary']
	current_temp = obj['hourly']['data'][0]['temperature']
	max_temp = obj['daily']['data'][0]['temperatureMax']
	min_temp = obj['daily']['data'][0]['temperatureMin']

	# Color coding is as follows:
	# 0 - very cold, 1 - cold, 2 - ok, 3 - hot, 4 - very hot
	if (current_temp <= -10):
		color_code = 0
	elif (current_temp <= 3):
		color_code = 1
	elif (current_temp <= 10):
		color_code = 2
	elif (current_temp <= 20):
		color_code = 3
	else:
		color_code = 4

	text = "The weather in <br><b>{0}</b><br> is {1}<br>Current temperature = {2}<br>Max temp = {3}<br>Min temp = {4}".format(place.encode('utf-8'), current_summary, current_temp, max_temp, min_temp)

	return json.dumps({
						"currentSum": current_summary,
						"dailySummary": daily_summary,
						"currentTemp": current_temp,
						"maxTemp": max_temp,
						"minTemp": min_temp,
						"coldIndex": color_code,
						"text": text,
						"place": place
	})

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(debug = True, port = port)
