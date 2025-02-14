# Import the dependencies.
from flask import Flask, jsonify
import numpy as np
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import warnings

#################################################
# Database Setup
#################################################

# Create engine to connect to the SQLite database
engine = create_engine("sqlite:///../Resources/hawaii.sqlite")  # Adjusted path

# Reflect an existing database into a new model
Base = automap_base()

# Suppress reflection warning for SQLAlchemy <2.0
with warnings.catch_warnings():
    warnings.simplefilter("ignore", category=DeprecationWarning)
    Base.prepare(engine, reflect=True)  # Use reflect=True for compatibility

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################

app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    """List all available API routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation - Last 12 months of precipitation data<br/>"
        f"/api/v1.0/stations - List of weather stations<br/>"
        f"/api/v1.0/tobs - Temperature observations for the most active station<br/>"
        f"/api/v1.0/&lt;start&gt; - Min, Avg, Max temperatures from start date<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt; - Min, Avg, Max temperatures for date range"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the last 12 months of precipitation data as JSON."""
    session = Session(engine)

    # Find the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query precipitation data for the last 12 months
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d")).all()

    session.close()

    # Convert to dictionary format
    precip_dict = {date: prcp for date, prcp in results}
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of weather stations."""
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert to list
    stations_list = list(np.ravel(results))
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return temperature observations of the most active station for the last year."""
    session = Session(engine)

    # Find the most active station
    most_active_station_id = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

    # Find the most recent date
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = dt.datetime.strptime(most_recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query last 12 months of temperature observations for the most active station
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station_id).\
        filter(Measurement.date >= one_year_ago.strftime("%Y-%m-%d")).all()

    session.close()

    # Convert to list of dictionaries
    tobs_list = [{date: temp} for date, temp in results]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_range(start, end=None):
    """Return min, avg, and max temperature for a given start date or range."""
    session = Session(engine)

    # Define the query selection
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
    else:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()

    session.close()

    # Convert query result to a list
    temp_data = list(np.ravel(results))
    return jsonify(temp_data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
