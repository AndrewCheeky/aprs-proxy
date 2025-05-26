from flask import Flask, request, jsonify
import socket

app = Flask(__name__)

CALLSIGN = "6Y5KW-13"
PASSCODE = "10224"
APRS_SERVER = "rotate.aprs2.net"
APRS_PORT = 14580

@app.route('/sendaprs', methods=['POST'])
def send_aprs():
    try:
        data = request.get_json()
        callsign = data.get('callsign', CALLSIGN)
        aprs_data = data.get('data')

        if not aprs_data:
            return jsonify({"status": "error", "message": "No data field found"}), 400

        full_packet = f"{callsign}>APRS,TCPIP*: {aprs_data}"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((APRS_SERVER, APRS_PORT))
        s.send(f"user {callsign} pass {PASSCODE} vers WXBridge 1.0\n".encode())
        s.send((full_packet + '\n').encode())
        s.close()

        return jsonify({"status": "success", "packet": full_packet}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
