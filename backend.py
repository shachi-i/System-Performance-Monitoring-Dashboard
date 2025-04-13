import datetime
import collections
import pandas as pd
import psutil
import joblib
from flask import Flask, jsonify

app = Flask(__name__)


model = joblib.load("anomaly_detector.pkl")


cpu_history = collections.deque(maxlen=10)
memory_history = collections.deque(maxlen=10)

def get_system_metrics():
    """Collects real-time CPU, memory, and disk I/O metrics with correct feature names and order."""
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_io = float(psutil.disk_io_counters().read_bytes)

    
    cpu_history.append(cpu_usage)
    memory_history.append(memory_usage)

    
    cpu_moving_avg = sum(cpu_history) / len(cpu_history) if cpu_history else cpu_usage
    memory_moving_avg = sum(memory_history) / len(memory_history) if memory_history else memory_usage

    
    cpu_std = (sum([(x - cpu_moving_avg) ** 2 for x in cpu_history]) / len(cpu_history))**0.5 if len(cpu_history) > 1 else 0
    memory_std = (sum([(x - memory_moving_avg) ** 2 for x in memory_history]) / len(memory_history))**0.5 if len(memory_history) > 1 else 0

    
    now = datetime.datetime.now()
    day = now.weekday()  
    hour = now.hour  

    
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_io": disk_io,
        "hour": hour,
        "day": day,
        "cpu_moving_avg": cpu_moving_avg,
        "cpu_std": cpu_std,
        "memory_moving_avg": memory_moving_avg,
        "memory_std": memory_std
    }

@app.route("/monitor", methods=["GET"])
def monitor():
    """Collects system performance data and predicts anomalies."""
    data = get_system_metrics()

    
    feature_order = ['cpu_usage', 'memory_usage', 'disk_io', 'hour', 'day', 
                     'cpu_moving_avg', 'cpu_std', 'memory_moving_avg', 'memory_std']
    df = pd.DataFrame([data])[feature_order]  
    
    
    prediction = model.predict(df)
    data["anomaly"] = int(prediction[0])  
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
