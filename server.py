from model import AirportCode, connect_to_db, db
from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

import requests
import json
import datetime

from xml.etree import ElementTree

app = Flask(__name__)

app.secret_key = "Susan Secret Key"

@app.route("/")
def homepage():
	
	return render_template("base.html")


# DIS BE FOR THE AUTOCOMPLETE FUNCTION TO SEARCH FOR AIRPORT CODES
# CURRENTLY SENDING THE SUGGESTION LIST, BUT HAVEN'T FIGURED OUT THE JS SIDE
# NO DROP DOWN MENU ON WEBPAGE FOR THE SUGGESTIONS
@app.route("/autocomplete")
def autocomplete():
	search_value = request.args.get('term')
	print search_value
	query = AirportCode.query.filter(db.or_(AirportCode.code.contains(search_value), 
											AirportCode.location.contains(search_value))).all()
	suggestion_dict = []
	for item in query:
		code = item.code
		location = item.location
		suggestion_string = "(%s) %s" %(code, location)
		suggestion_dict.append(suggestion_string)
		code_loc_dict = {"code": code, "location": location}
	print suggestion_dict
	return jsonify(data=suggestion_dict)


@app.route("/airfaresearch")
def airfare_search():
	origin = request.args.get('origin')
	earliest_departure = request.args.get('earliest-departure-date')
	latest_departure = request.args.get('latest-departure-date')
	print earliest_departure, latest_departure
	length_of_stay = int(request.args.get('length-of-stay'))
	max_budget = request.args.get('max-budget')


	# below link for the Hotwire API
	# base_url = "http://api.hotwire.com/v1/tripstarter/air?apikey=dbmnd3ph48j6x5e5y8jbkuzn"
	# final_url= "%s&origin=%s&price=*~%s" % (
	# 	base_url, origin, max_budget)

	headers = {"Authorization": "Bearer T1RLAQL/QfI2vTvwGfizaSk3pXYlMh5wFRA9+OLqQ/h/YpxelgqOaRpqAACgtWo5h/kal3de+BbK0myvIVkRW3Wrf4lMaGiqZUHe4EzdEMYR/sicpLqBE/bjRUcdTwm3RhBVTUdWPEmwboT+LgPLZlEqILTUTNV7TC4B8/IuUvh6Apgjf0UWZVrxJr/lvVA00gD/+Zu7AGt/NljQg+TdaXX3HxWFbO9MaxJG9+pxfaifdUEATwb+i2I5kRUmrlwgDUUnz8hkc1lIYtN+xg**",
	"X-Originating-Ip": "50.197.129.150"}

	base_url = "https://api.test.sabre.com/v2/shop/flights/fares?"
	param_url = "origin=%s&earliestdeparturedate=%s&latestdeparturedate=%s&lengthofstay=%s&maxfare=%s&pointofsalecountry=US" % (
					origin, earliest_departure, latest_departure, length_of_stay, max_budget)
	final_url = base_url + param_url

	response = requests.get(final_url, headers=headers)

	response_json = response.json()

	# fare_dictionary = {}
	# for item in response_json["FareInfo"]:
	# 	destination = item.get("DestinationLocation")
	# 	low_nonstop_fare = item.get("LowestNonStopFare").get("Fare")
	# 	depart_date = item.get("DepartureDateTime")
	# 	return_date = item.get("ReturnDateTime")
	# 	about_fare_dict = {"destination": destination, 
	# 						"low_nonstop_fare": low_nonstop_fare,
	# 						"depart_date": depart_date,
	# 						"return_date": return_date}
	# 	fare_dictionary[destination] = about_fare_dict
	# print fare_dictionary

	return jsonify(response_json)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()