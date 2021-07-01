import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resouces/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

#Session Link
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def Home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"Precipitation: /api/v1.0/precipitation<br/>"
        f"Stations: /api/v1.0/stations<br/>"
        f"Temperatures: /api/v1.0/tobs<br/>"
        f"Start Date: /api/v1.0/<start><br/>"
        f"End Date: /api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def Precipitation():
    ##do the same functions we did in jupyter notebook.
    ###find the date a year before the last data point in the DB
    date_year_back = session.data(measurement.date).order_by(measurement.date.desc())first()[0]
    previous_year = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=366)
    ####query for date and precipitation prcp
    data = session.data(measurement.date, measurement.prcp).\
        filter(measurement.date >= previous_year).all()

    #####convert the query to a dictionary with date as the key and prcp as the value
    ######Return a JSON of the dictionary

    precip_data = []
    for i, prcp in data:
        data = {}
        data['date'] = i
        data['prcp'] = prcp
        precip_data.append(data)

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def Stations():
    data = session.data(station.name, station.station, station.elevation).all()

    #dictionary for JSON
    station_list = []
    for i in data:
        row = {}
        row['name'] = i[0]
        row['stations'] = i[1]
        row['elevation'] = i[2]
        station_list.append(row)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def Temperatures():
    data = session.data(station.name, measurement.date, measurement.tobs).\
        filter(measurement.date >= "2017-01-01", measurement.date <= "2018-01-01")
        all()

    #dictionary for JSON
    tobs_list = []
    for i in data:
        row = {}
        row["Date"] = i[1]
        row["Stations"] = i[0]
        row["Temperature"] = int(i[2])
        tobs_list.append(row)
        
    return jsonify(tobs_list)