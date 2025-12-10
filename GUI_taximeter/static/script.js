// Esta función envía órdenes a Python (Start, Stop, etc.)
function sendCommand(action) {
    fetch('/action/' + action);
}

// Esta función pregunta a Python "¿Cuánto es?" y actualiza la pantalla
function updateDisplay() {
    fetch('/status')
        .then(response => response.json())
        .then(data => {
            // 1. Actualizar el precio
            document.getElementById('fare-display').innerText = data.fare.toFixed(2);
            
            // 2. Actualizar el texto del estado
            let statusText = data.active ? data.status.toUpperCase() : "LIBRE / OFF";
            if (data.status === 'finished') statusText = "COBRADO";
            document.getElementById('state-text').innerText = statusText;

            // 3. Cambiar luces de colores (cambiando la clase CSS)
            const indicator = document.getElementById('status-indicator');
            // Quitamos clases viejas y ponemos la nueva (stopped o moving)
            indicator.className = 'status-text ' + data.status;
        })
        .catch(error => console.log("Error de conexión con el taxi:", error));
}

// ¡Preguntar a Python cada 500 milisegundos (medio segundo)!
setInterval(updateDisplay, 500);