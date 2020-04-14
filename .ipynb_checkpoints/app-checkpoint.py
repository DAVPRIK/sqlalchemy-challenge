
#################################################
# Flask Application
#################################################

# Dependencies and Setup
import os

import pandas as pd
import numpy as np

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


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///hawaii.sqlite"

db = SQLAlchemy(app)


engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save reference to the table

# Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/stationlist<br/>"

        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"



       
    )


@app.route("/api/v1.0/precipitation")

# def precipitation():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of all passenger names"""
#     # Query all passengers
#     results = session.query(Measurement.station).all()

#     session.close()

#     # Convert list of tuples into normal list
#     all_names = list(np.ravel(results))

#     return jsonify(all_names)


@app.route("/api/v1.0/stations")
def name():
    # Create our session (link) from Python to the DB
    # session = Session(db.engine)
    """Return a list of all category names"""
    # Query all categories
    results = db.session.query(Station.name).all()
    db.session.close()
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
    print(all_names)
    return jsonify(all_names)


# @app.route("/api/v1.0/stationslist")
# def stations():
#     # Create our session (link) from Python to the DB
#     session = Session(engine)

#     """Return a list of station data """
#     # Query all stations
#     results = session.query(Station.id, Station.station,Station.name,Station.latitude,Station.longitude,\
#         Station.elevation).all()


#     session.close()

#     # Create a dictionary from the row data and append to a list of all_passengers
#     all_stations = []
#     for id, station, name,latitude,longitude,elevation in results:
#         station_dict = {}
#         station_dict["id"] = id
#         station_dict["station"] = station
#         station_dict["name"] = name
#         station_dict["latitude"] = latitude
#         station_dict["longitude"] = longitude
#         station_dict["elevation"]=elevation

#         all_stations.append(station_dict)

#     return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
