from flask import Flask, request
import subprocess
import json

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    alert = request.json
    print(json.dumps(alert, indent=4))  # Log for demo
    # Trigger Ansible playbook
    subprocess.run(['ansible-playbook', '/opt/ansible/recover.yml'])
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
