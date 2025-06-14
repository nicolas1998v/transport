# 🚇 London Transport Data Projects

This repository contains two Streamlit live dashboards analyzing London Underground data, both powered by the [Transport for London (TfL) API](https://api-portal.tfl.gov.uk/):

- [Journey Time Heatmap](#journey-time-heatmap) ([Live App URL](https://bigbendashboard.streamlit.app/))
- [Prediction Error Dashboard](#prediction-error-dashboard) ([Live App URL](https://kingscrossdashboard.streamlit.app/))

---

## What These Projects Have in Common

- **Cloud-Native Evolution:**  
  Both projects began as Google Cloud Functions but were migrated to Google Cloud VMs for cost savings.
- **Cost Optimization:**  
  A Google Cloud Scheduler job starts the VM in the morning and stops it at night, so the VM only runs during required hours—significantly reducing compute charges.
- **Service Management:**  
  Each VM uses a `systemd` service file to manage the main script, specifying the working directory, Python environment, and all necessary files. This ensures the script starts automatically on VM boot and can be easily restarted or monitored.
- **TfL API:**  
  Both projects use the Transport for London API, but each targets different endpoints and analyses.
- **Data Processing:**  
  Both projects required significant data wrangling, filtering, and anomaly detection to ensure high-quality, actionable insights.

---

# [Journey Time Heatmap](https://bigbendashboard.streamlit.app/)

This Streamlit dashboard visualizes journey times from the Houses of Parliament (SW1A 2JR) to all London postcodes, using a color-coded heatmap to highlight areas with faster or slower public transport connections.

## ⚠️ Data Availability

> **Note:**  
> You cannot run this project locally out-of-the-box because the raw and filtered postcode datasets are too large to include in the repository.
> - **Raw Data:** [Download here](https://www.doogal.co.uk/london_postcodes)
> - **Filtered Data:** Contact me for access.

## Data Preparation

- **Postcode Dataset:**  
  Started with a comprehensive CSV of London postcodes sourced online.
- **Filtering:**  
  I performed extensive testing to identify and remove postcodes that consistently failed to return valid journey times, resulting in a high-quality, filtered dataset.

## Anomaly Detection

- The dashboard applies a **k-nearest neighbors (KNN)** algorithm:
  - For each postcode, the journey time is compared to its 12 nearest neighbors (by latitude and longitude).
  - Points with journey times that differ significantly from their neighbors are filtered out as anomalies.
  - This process removes outliers and ensures the heatmap reflects realistic travel times across London.

## Features

- **Interactive Heatmap:** Visualizes journey times to every postcode in London using Folium and Streamlit.
- **Live Data:** Loads the latest journey time results from Google Cloud Storage.
- **Anomaly Filtering:** Uses k-nearest neighbors to filter out anomalous journey times.
- **Statistics:** Displays summary statistics (mean, median, 95th percentile) for journey times.
- **Batch Processing:** Combines results from multiple data batches for each update.

## How It Works

1. **Data Loading:** Loads the latest journey time results from Google Cloud Storage, merging them with the filtered postcode dataset.
2. **Anomaly Filtering:** The KNN-based filter removes outlier points.
3. **Visualization:** The filtered data is plotted on a Folium map, with color indicating journey duration.
4. **Statistics:** Key metrics are displayed alongside the map.

---

# [Prediction Error Dashboard](https://kingscrossdashboard.streamlit.app/)

This dashboard analyzes and visualizes prediction errors for London Underground trains serving King's Cross, using data from the TfL API and Google BigQuery.

## Data Journey

- **Understanding the Data:**  
  I first had to understand the structure and quirks of the TfL data.  
  I had to go through a long phase of data cleaning, excluding the circle line due to data quality issues, excluding some Terminus stations in which the train is on standby and still predicting, and understanding the different glitches of the API.  
  To isolate individual train runs and remove glitches, I developed a query that checked for observations, allowing me to segment continuous data into distinct runs.
- **Data Collection:**  
  - **Initial Approach:** I started by making API requests every minute.
  - **Optimization:** To better capture arrivals and anomaly magnitudes, I switched to every 30 seconds. However, this sometimes wasn't enough to process all data when there were many lengthy arrivals, so I increased the interval to 33 seconds, which proved to be the best balance between arrival detection and processing time.

## BigQuery Tables

- **predictions_history:**  
  The main table gathering all raw prediction data.
- **initial_errors:**  
  Contains only the first prediction for each train run (the "initial prediction").
- **any_errors:**  
  Contains all predictions for each run (the "any prediction").
  
### Table Columns

- `train_id`: Unique identifier for each train.
- `timestamp`: Time of the prediction.
- `arrival_timestamp`: Actual arrival time.
- `line`: Tube line.
- `direction`: Direction of travel.
- `error_seconds`: Prediction error in seconds.
- `time_to_station`: Time to station in seconds.
- `current_location`: Text description of the train's location.
- `initial_prediction_timestamp`: timestamp of the initial prediction
- `any_prediction_timestamp`: timestamp of any prediction
- ...and other relevant fields.

## Features

- **Live Data:** Fetches and updates data from the TfL API every 33 seconds.
- **BigQuery Integration:** Stores and queries large volumes of prediction data efficiently.
- **Interactive Visualizations:** Explore prediction errors, accuracy by line, time, location, and more.
- **Correlation & Error Analysis:** Understand how prediction errors relate to time to station and other factors.
- **Event & Weather Impact:** Analyze how external factors affect prediction accuracy.

## Cost Optimization

The system is optimized for cost efficiency:

### Data Collection (Cloud Function)
- Processes data in 1 hour 40 minute windows to capture even very late train journeys
- Reduces BigQuery costs by limiting data scans
- Daily processing cost: ~$0.12 to $0.25
- Monthly cost: ~$3.60 to $7.50
- Yearly cost: ~$43.20 to $90.00

### Dashboard (Streamlit)
- Uses Redis caching to store query results for 1 hour
- Dashboard refreshes every hour for 14 hours per day
- Processes 10-15 queries per refresh (140-210 queries daily)
- Daily dashboard cost: ~$0.01 to $0.02
- Monthly dashboard cost: ~$0.30 to $0.60
- Yearly dashboard cost: ~$3.60 to $7.20

Total System Cost:
- Daily: ~$0.13 to $0.27
- Monthly: ~$3.90 to $8.10
- Yearly: ~$46.80 to $97.20

## Dashboard Tabs

- **Prediction Analysis:** Correlation matrices and scatter plots for prediction errors.
- **Initial Prediction Analysis:** Focus on the first prediction for each train.
- **Line & Time Analysis:** Accuracy by line, hour, and day of week.
- **Prediction Precision Analysis:** Accuracy by time to station.
- **Location Analysis:** Heatmaps of accuracy by station.
- **Direction, Peak Times, Error Pattern, Drift, Anomaly, Line Interaction, Weather, Event Impact:** Specialized analyses for deeper insights.

---

## 🖥️ Running the Apps Locally

### Prerequisites

- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [Folium](https://python-visualization.github.io/folium/) (for heatmap)
- [scikit-learn](https://scikit-learn.org/) (for heatmap)
- [Google Cloud Storage Python Client](https://googleapis.dev/python/storage/latest/index.html)
- [Google Cloud BigQuery Python Client](https://googleapis.dev/python/bigquery/latest/index.html) (for predictions)
- Other dependencies in `requirements.txt`
- Google Cloud service account credentials (added to Streamlit secrets for cloud deployment)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/nicolas1998v/transport.git
cd transport

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run heatmap/dashboard.py      # For the heatmap
streamlit run prediction/dashboard.py   # For the prediction dashboard
```
For both projects you would need to set a micro-VM for each and copy the service, run and main files inside the VM to the appropriate locations. 

Also you would need to have a service account with 
- BigQuery Admin
- Compute Instance Admin (v1)
- Storage Admin roles. And retrieve a key and place it in the VM.

You would need to retrieve many keys from the Transport for London API (by creating many accounts).
For the heatmap you would need to filter the data to get valid postcodes.  
For the predictions you would need to create 3 tables in Bigquery and set up API connections to Ticketmaster and WeatherMap API by adding appropriate keys in the .env file.  
The events and weather data collection is done through Cloud Functions as its simpler, and scheduled by Cloud Scheduler.

---

## 🙏 Acknowledgments

- Transport for London for open data.
- OpenWeatherMap API for weather data
- TicketMaster API for event data
- London postcode data sourced from doogal.co.uk.
- Google Cloud VM, systemd,and Cloud Scheduler for robust, cost-effective deployment.
- My brother Juan Pablo for proving me guidance throughout this past year.
