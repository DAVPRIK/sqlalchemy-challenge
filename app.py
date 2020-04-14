#################################################
# Flask Application
#################################################

# Dependencies and Setup
import os

import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, and_
from sqlalchemy import Column, Integer, Float, String
from flask import Flask, jsonify, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Database Setup
#################################################


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Resources/hawaii.sqlite"

db = SQLAlchemy(app)


engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save reference to the table

Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """ Home page
    List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
		f"/api/v1.0/start<br/>"
		f"/api/v1.0/start/end<br>"
        
         )

# Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def precipitation():
	# Query all Measurments
	results = db.session.query(Measurement).all()
	# Close the Query
	db.session.close()

	#Create a dictionary using 'date' as the key and 'prcp' as the value.
	prcp = []
	for result in results:
		prcp_dict = {}
		prcp_dict["date"] = result.date
		prcp_dict["prcp"] = result.prcp
		prcp.append(prcp_dict)

	# Jsonify summary
	return jsonify(prcp)


# Return a JSON list of stations from the dataset.

@app.route("/api/v1.0/stations")
def stationlist():
        
    # Query all stations
    results = db.session.query(Station.name).all()
    db.session.close()
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    print(all_names)
    return jsonify(all_names)

# /api/v1.0/tobs

# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route("/api/v1.0/tobs")
def temperature():
	# Find last date in database then subtract one year
	prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

	# Query tempurature observations
	temperature_results = db.session.query(Measurement.tobs)\
        .filter(Measurement.date > prev_year).all()
	# Close the Query
	db.session.close()

	# Convert list of tuples into normal list
	temperature_list = list(np.ravel(temperature_results))

	# Jsonify summary
	return jsonify(temperature_list)

# @app.route("/api/v1.0/tobs")
# def temperature():
#     date_str= db.session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    
#     recentdate = db.session.query(datetime.strptime(date_str, '%Y-%m-%d').date())
#     # Find last date in database then subtract one year
#     prev_year = dt.date(recentdate) - dt.timedelta(days=365)

# 	# Query tempurature observations

#     most_active_tobs = db.session.query(Measurement.tobs).\
#     filter(Measurement.date >= prev_year).filter(Measurement.station=='USC00519281').all()

#     db.session.close()

# 	# Convert list of tuples into normal list
#     temperature_list = list(np.ravel(most_active_tobs))

# 	# Jsonify summary
#     return jsonify(temperature_list)


# /api/v1.0/<start> and /api/v1.0/<start>/<end>


# Return a JSON list of the minimum temperature, the average temperature, 
# and the max temperature for a given start or start-end range.

# When given the start only, calculate TMIN, TAVG, and TMAX for all dates 
# greater than and equal to the start date.


@app.route("/api/v1.0/<start>")

def greater_start_date(start):

	start_trip_date_temps = []

	summary_stats = db.session.query(func.min(Measurement.tobs),\
		func.max(Measurement.tobs),func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date >= start).all()

	db.session.close()
	start_trip_date_temps = list(np.ravel(summary_stats))

	return jsonify(start_trip_date_temps)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates between 
# the start and end date inclusive.

@app.route("/api/v1.0/temp/<start>/<end>")


def start_end_trip(start, end):

	round_trip_temps = []

	summary_stats = db.session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),\
		func.round(func.avg(Measurement.tobs))).\
	filter(Measurement.date.between(start,end)).all()
	db.session.close()
	round_trip_temps = list(np.ravel(summary_stats))
	return jsonify(round_trip_temps)


if __name__ == '__main__':
    app.run(debug=True)












