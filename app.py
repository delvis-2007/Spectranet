import re
import subprocess
from flask import Flask, jsonify, render_template

# Initialize the official SpectraNet core application engine
app = Flask(__name__)


def get_average_signal():
    """Sniffs ambient Wi-Fi signal power using native Windows network utilities."""
    try:
        cmd = subprocess.check_output(
            ["netsh", "wlan", "show", "networks", "mode=bssid"],
            shell=True,
            text=True,
        )
        signals = re.findall(r"Signal\s+:\s+(\d+)%", cmd)
        if signals:
            int_signals = [int(s) for s in signals]
            return sum(int_signals) / len(int_signals)
        return 100  # Baseline clean signal if no networks are parsed
    except Exception:
        return 100


@app.route("/")
def index():
    # Serves the main SpectraNet graphical interface
    return render_template("index.html")


@app.route("/telemetry")
def telemetry():
    # Live API data stream consumed by the front-end rendering layer
    return jsonify({"ambient_power": get_average_signal()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
