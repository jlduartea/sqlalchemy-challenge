
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

####################
# Database Setup
####################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

###########################
# References to each table
###########################
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)

###############
# Flask setup
###############
app = Flask(__name__)

##################
# Defining Routes
##################
@app.route("/")
def home():
    return (
        f"<p>Alohaaa Welina... this es the Hawaii Weather Site</p>"
        f"<p>Available routes:</p>"
        f"<p>/api/v1.0/precipitation<br/>"
        f"<p>/api//v1.0/stations<br/>"
        f"<p>/api//v1.0/tobs<br/>"
        f"<p>/api//v1.0/<start>/<br/>"
        f"<p>/api/v1.0/<start>/<end><br>"
    )

###################    
# Precipitation
###################
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Perfoming Query Precip
    results = (session.query(Measurement.date, Measurement.tobs)
                      .order_by(Measurement.date))
    
    # Creating a dictionary
    precip_tobs_dict = []
    for i in results:
        date_dict = {}
        date_dict["date"] = i.date
        date_dict["tobs"] = i.tobs
        precip_tobs_dict.append(date_dict)

    return jsonify(precip_tobs_dict)

####################
# Stations
####################
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    # Perfoming Query Stats
    results = session.query(Station.name).all()

    # Create a list
    stats_list = list(np.ravel(results))

    return jsonify(stats_list)

###################
# TOBS
###################
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    # Perfoming Query Mesurements
    tobs = session.query(Measurement.tobs).\
    filter(Measurement.station=='USC00519281').\
    filter(Measurement.date >= '2016-08-24').\
    order_by(Measurement.date.desc()).all()
    tob_list = list(np.ravel(tobs))
    return jsonify(tob_list)

#######################
# Start
#######################
@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    
    results = (session.query(Measurement.tobs).filter(Measurement.date.between(start, '2017-08-23')).all())
    tobst_df = pd.DataFrame(results)

    tavg = tobst_df["tobs"].mean()
    tmax = tobst_df["tobs"].max()
    tmin = tobst_df["tobs"].min()
    
    return jsonify(tavg, tmax, tmin)

########################
# Start/End
########################
@app.route('/api/v1.0/<start>/<end>') 
def start_end(start, end):
    session = Session(engine)
    
    results = (session.query(Measurement.tobs).filter(Measurement.date.between(start, end)).all())
    tobst_df = pd.DataFrame(results)

    tavg = tobst_df["tobs"].mean()
    tmax = tobst_df["tobs"].max()
    tmin = tobst_df["tobs"].min()
 
    return jsonify(tavg, tmax, tmin)

if __name__ == "__main__":
    app.run(debug=True)

