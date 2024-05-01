from flask import Flask, request, jsonify
from scipy import interpolate
import pandas as pd

app = Flask(__name__)

# Load the log file into a DataFrame
# Load the log file into a DataFrame
log_file = "weather_data.txt"
df = pd.read_csv(log_file, delimiter='\t', parse_dates=['Timestamp'], infer_datetime_format=True)


# Convert timestamps to datetime objects
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# Interpolate temperature data
timestamps = pd.to_numeric(df['Timestamp'])
temperatures = df['Temperature (°C)']
interpolated_temperature = interpolate.interp1d(timestamps, temperatures, kind='linear', fill_value='extrapolate')

# API endpoint to get temperature for a given timestamp
@app.route("/temperature/<timestamp>")
def get_temperature(timestamp):
    try:
        timestamp = pd.to_datetime(timestamp)
        temperature = float(interpolated_temperature(pd.to_numeric(timestamp)))
        return jsonify({"timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S'), "temperature": temperature})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# API endpoint to get rain percentage for a given time range
@app.route("/rain_percentage")
def get_rain_percentage():
    try:
        start_timestamp = pd.to_datetime(request.args.get('start'))
        end_timestamp = pd.to_datetime(request.args.get('end'))
        time_range = df[(df['Timestamp'] >= start_timestamp) & (df['Timestamp'] <= end_timestamp)]
        total_time = (end_timestamp - start_timestamp).total_seconds() / 60  # Convert to minutes
        rain_time = time_range[time_range['Rain Presence'] == 1]['Rain Presence'].count() / 60  # Convert to minutes
        percentage = (rain_time / total_time) * 100
        return jsonify({"start_timestamp": start_timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
                        "end_timestamp": end_timestamp.strftime('%Y-%m-%d %H:%M:%S'), 
                        "rain_percentage": percentage})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
