from flask import Flask, render_template
from flask import request
from flask import jsonify
import requests
import asyncio
import os


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def home():
	return render_template('index.html')


@app.route('/search')
def search():
	inp = request.args['input']
	url = 'https://www.swiggy.com/dapi/misc/places-autocomplete?input=' + str(inp) + "&types="	
	return requests.get(url).json()

@app.route('/geocode')
def geocode():
	placeid = request.args['placeid']
	url = "https://www.swiggy.com/dapi/misc/reverse-geocode?place_id=" + str(placeid)	
	return requests.get(url).json()

@app.route('/restaurants')
def restaurants():
	lat = request.args['lat']
	lon = request.args['long']
	os.chdir('C:\\Users\\hp\\Desktop\\My Projects\\Restaurants\\website')
	import getrestlist1
	asyncio.set_event_loop(asyncio.SelectorEventLoop())
	loop = asyncio.get_event_loop()
	js = loop.run_until_complete(getrestlist1.getrest(lat, lon))
	return jsonify(js)

if __name__=="__main__":
	app.run(debug=True)
