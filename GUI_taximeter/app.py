from flask import Flask, render_template, jsonify
import time

app = Flask(__name__)

# CONFIGURACIÓN
RATES = {"stopped": 0.02, "moving": 0.05}

# ESTADO DEL TAXI
taxi_state = {
    "is_active": False,
    "status": "stopped",
    "start_time": 0,
    "accumulated_fare": 0.0
}

def calculate_current_fare():
    if not taxi_state["is_active"]:
        return taxi_state["accumulated_fare"]
    
    now = time.time()
    duration = now - taxi_state["start_time"]
    current_rate = RATES[taxi_state["status"]]
    added_fare = duration * current_rate
    
    return taxi_state["accumulated_fare"] + added_fare

@app.route("/")
def home():
    # Flask buscará este archivo dentro de la carpeta 'templates'
    return render_template("index.html")

@app.route("/status")
def get_status():
    fare = calculate_current_fare()
    return jsonify({
        "fare": round(fare, 2),
        "status": taxi_state["status"],
        "active": taxi_state["is_active"]
    })

@app.route("/action/<command>")
def handle_action(command):
    global taxi_state
    now = time.time()
    
    if command == "start":
        if not taxi_state["is_active"]:
            taxi_state["is_active"] = True
            taxi_state["status"] = "stopped"
            taxi_state["start_time"] = now
            taxi_state["accumulated_fare"] = 0.0
            
    elif command in ["move", "stop"]:
        if taxi_state["is_active"]:
            duration = now - taxi_state["start_time"]
            rate = RATES[taxi_state["status"]]
            taxi_state["accumulated_fare"] += duration * rate
            taxi_state["status"] = "moving" if command == "move" else "stopped"
            taxi_state["start_time"] = now

    elif command == "finish":
        if taxi_state["is_active"]:
            final_fare = calculate_current_fare()
            taxi_state["accumulated_fare"] = final_fare
            taxi_state["is_active"] = False
            taxi_state["status"] = "finished"

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)