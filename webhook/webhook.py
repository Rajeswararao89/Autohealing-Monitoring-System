from flask import Flask, request, jsonify
import subprocess
import logging

app = Flask(__name__)

# Setup logging
logging.basicConfig(
    filename='/var/log/autoheal-webhook.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Mapping alerts to their respective Ansible playbooks
PLAYBOOKS = {
    "NginxDown": "/etc/ansible/nginx_autoheal.yml",
    "MySQLDown": "/etc/ansible/mysql_autoheal.yml"
}

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json
    logging.info(f"Received alert payload: {data}")

    try:
        for alert in data.get("alerts", []):
            alertname = alert["labels"].get("alertname")
            playbook = PLAYBOOKS.get(alertname)

            if playbook:
                logging.info(f"Triggering playbook {playbook} for alert {alertname}...")
                result = subprocess.run(
                    ["ansible-playbook", playbook],
                    capture_output=True, text=True
                )
                logging.info(result.stdout)
                logging.error(result.stderr)
                logging.info(f"Auto-heal for {alertname} completed.")
            else:
                logging.warning(f"No playbook mapped for alert: {alertname}")

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error handling alert: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
