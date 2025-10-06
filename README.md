# Plant Watering Automation

Champlain IoT — Raspberry Pi Plant Monitoring and Automation System  

- [Plant Watering Automation](#plant-watering-automation)
  - [Source](#source)
  - [Getting Started](#getting-started)
  - [Questions or Issues?](#questions-or-issues)
  - [Development Notes](#development-notes)
- [Hardware Setup](docs/hardware-setup.md)
- [MQTT Configuration](docs/mqtt-config.md)
- [Flask and Socket.IO Overview](docs/flask-socketio.md)
- [Data Logging Structure](docs/data-storage.md)
- [System Diagram](docs/system-diagram.md)
- [Future Improvements](docs/future-work.md)

---

## Source

This project is an implementation of a **Raspberry Pi–based plant monitoring and watering system**.  
It uses **Flask**, **MQTT**, and **Socket.IO** to collect, display, and store environmental sensor data.  
The Raspberry Pi listens for MQTT messages from external sensors, logs the readings to daily JSON files, and streams live updates to a web dashboard.  

The system can be extended to control a **solenoid valve or pump**, enabling fully automated watering when soil moisture drops below a threshold.

---

## Getting Started

1. **Setup Environment**  
   - Ensure your Raspberry Pi is running Python 3.  
   - Ensure your raspberry pi is wired properly including the solenoid valve and the moisture sensor.  
   - Install required dependencies:  
     ```bash
     pip install flask flask-socketio paho-mqtt
     ```

2. **Configure MQTT Broker**  
   - Edit the following in `app.py`:  
     ```python
     MQTT_BROKER = "192.168.xxx.xxx"
     MQTT_PORT = 1883
     MQTT_TOPIC = "plant_monitor/data"
     ```  
   - Confirm your microcontroller or sensor node is publishing data to this topic.

3. **Run the Application**  
   - Start the Flask server:  
     ```bash
     python3 app.py
     ```  
   - Access the dashboard at `http://<raspberry-pi-ip>:5000`

4. **View Historical and Live Data**  
   - **Live Data**: Displays real-time temperature, humidity, or soil readings.  
   - **Historical Data**: Lists JSON files saved daily in the `/data` directory.  

---

## Questions or Issues?

If you have questions about setup or need clarification on any part of the system, please:

1. Check the Flask routes and MQTT handlers in `app.py`
2. Contact me


---

**Remember**:  
Following the documentation and setup process carefully will ensure stable communication between your Raspberry Pi, sensors, and web interface.

---

## Development Notes

- The MQTT listener runs on a **separate thread** to avoid blocking the Flask application.  
- Daily log files are stored under `/data` in the format `YYYY-MM-DD.json`.  
- When adding new sensors or expanding the system, ensure their MQTT payloads are compatible with the JSON logging structure.  
- If `socketio.emit` is not sending updates, verify both Flask-SocketIO and the MQTT client are initialized correctly.
