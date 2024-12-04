import json
import os
import datetime
import paho.mqtt.client as mqtt
from flask import Flask, render_template, request, send_from_directory, redirect, session, flash, url_for
from flask_socketio import SocketIO
import threading

# Create the Flask app
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable cross-origin requests if needed
app.secret_key = 'your_secret_key'  # Required for session management

USERNAME = 'admin'
PASSWORD = 'password'

# MQTT Configuration
MQTT_BROKER = "192.168.227.165"  # Replace with your MQTT broker address
MQTT_PORT = 1883
MQTT_TOPIC = "plant_monitor/data"

# Set the data folder path
DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)  # Ensure the data directory exists

# MQTT client setup
mqtt_client = mqtt.Client()

@app.route('/')
def home_func():
    if 'username' in session:
        return render_template('base.html', title="Dashboard")  # Show original content
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            session['username'] = username
            return redirect(url_for('home_func'))  # Redirect to the main content
        else:
            flash('Invalid Credentials. Please try again.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Define the route for live data
@app.route('/live')
def live_func():
    return render_template('live-data.html', title="Live Data")

@app.route('/pump')
def pump_func():
    return render_template('pumpdata.html', title="Pump Data")

@app.route('/historical')
def historical_func():
    files = os.listdir(DATA_FOLDER)
    search = request.args.get('search')
    if search:
        files = [f for f in files if search in f]
    return render_template('historicaldata.html', title="Historical Data", files=files)

@app.route('/view-file/<file_name>')
def view_file(file_name):
    try:
        return send_from_directory(DATA_FOLDER, file_name)
    except FileNotFoundError:
        return "File not found", 404

# Handle incoming MQTT messages and save to a daily file
def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload)
        if data:
            # Create the filename using the current date
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            file_path = os.path.join(DATA_FOLDER, f"{current_date}.json")

            # Check if the file exists, if not, create a new one
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    existing_data = json.load(f)
            else:
                existing_data = []

            # Append the new data to the existing file data
            existing_data.append(data)

            # Write the updated data back to the file
            with open(file_path, "w") as f:
                json.dump(existing_data, f, indent=4)

            # Emit data for both humidity and temperature
            if 'temperature' in data and 'humidity' in data:
                socketio.emit('new_data', {'temperature': data['temperature'], 'humidity': data['humidity']})
    except Exception as e:
        print(f"Error in on_message: {e}")

# MQTT setup
mqtt_client.on_message = on_message
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
mqtt_client.subscribe(MQTT_TOPIC)

# Start the MQTT loop in a separate thread
def mqtt_loop():
    mqtt_client.loop_forever()

mqtt_thread = threading.Thread(target=mqtt_loop)
mqtt_thread.daemon = True
mqtt_thread.start()

# Run the Flask app with Socket.IO
if __name__ == '__main__':
    socketio.run(app, debug=True)
