# add dependencies
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# set up database
engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Add Variable for each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a Session link from Python to our database
session = Session(engine)

# Set up Flask
app = Flask(__name__)

# Identify Welcome Route
# When creating routes, we follow the naming convention /api/v1.0/ followed by the name of the route. 
# This convention signifies that this is version 1 of our application. 
# This line can be updated to support future versions of the app as well.

@app.route('/')
def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    <br>Available Routes:<br>
    <br>/api/v1.0/precipitation<br>
    <br>/api/v1.0/stations<br>
    <br>/api/v1.0/tobs<br>
    <br>/api/v1.0/temp/start/end<br>
    ''')

# Add a route
@app.route("/api/v1.0/precipitation")
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
filter(Measurement.station == 'USC00519281').\
filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)


@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start, end):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           

    if not end: 
        results = session.query(*sel).\
        filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)