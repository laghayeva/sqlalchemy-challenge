# SQLAlchemy Challenge – Climate Analysis

## Overview
This project analyzes historical climate data for **Honolulu, Hawaii**, using **SQLAlchemy ORM, SQLite, Pandas, Matplotlib, and Flask**. The goal is to retrieve, visualize, and serve climate data through a Flask API.

---

## Repository Location
**GitHub Repository:** https://github.com/laghayeva/sqlalchemy-challenge

---


## Code Source
All code was written by me with the help of some research resources.

---

## Project Tasks
This challenge is divided into two main sections:

### ** Climate Data Analysis (Jupyter Notebook)**
Performed **exploratory data analysis** on climate data from an SQLite database:
- **Precipitation Analysis**:
  - Retrieved the last **12 months of precipitation data**.
  - Stored results in a Pandas DataFrame and plotted precipitation trends.
- **Station Analysis**:
  - Identified the **most active weather stations**.
  - Retrieved temperature observations for the most active station.
  - Plotted temperature distribution using a histogram.

### ** Flask API Development**
Built a **Flask API** to serve climate data:
- **Available Routes**:
  - `/` - Lists all available API endpoints.
  - `/api/v1.0/precipitation` - Returns the last 12 months of precipitation data.
  - `/api/v1.0/stations` - Returns a list of all weather stations.
  - `/api/v1.0/tobs` - Returns temperature observations for the most active station.
  - `/api/v1.0/<start>` - Returns min, avg, and max temperatures from the start date onward.
  - `/api/v1.0/<start>/<end>` - Returns min, avg, and max temperatures for a date range.

---

## Technologies Used
- **Python**
- **SQLAlchemy ORM**
- **SQLite Database**
- **Flask**
- **Pandas**
- **Matplotlib**
- **Jupyter Notebook**

---
