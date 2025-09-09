# Self-Healing Infrastructure with Prometheus, Alertmanager, and Ansible
### Overview
This project implements a self-healing infrastructure to automatically detect and recover from service failures. It monitors an NGINX web server for uptime and system CPU usage, using Prometheus for metric collection, Alertmanager for alerting, and Ansible for automated recovery. When failures occur (e.g., NGINX down or CPU > 90%), alerts trigger an Ansible playbook to restart the service or system. The setup runs on an Ubuntu 22.04 VM, with a Flask webhook bridging Alertmanager and Ansible.

### Features

- Monitors NGINX uptime and system CPU usage.
- Alerts on service downtime (1-minute threshold) or high CPU (>90% for 2 minutes).
- Automated recovery via Ansible playbook to restart NGINX or reboot the system.
- Webhook integration for real-time alert handling.
- Comprehensive documentation, including a LaTeX report (self_healing_report.tex).

### Prerequisites

- Ubuntu 22.04 LTS (VM or native).
- Internet access for package installation.
- Sudo privileges.
- Tools: Git, Prometheus, Alertmanager, Ansible, NGINX, Flask, Node Exporter, NGINX Prometheus Exporter.

### Directory Structure
self-healing-infra

├── ansible\
│   └── recover.yml        
├── alertmanager\
│   └── alertmanager.yml    
├── prometheus\
│   ├── prometheus.yml      
│   └── rules.yml           
├── webhook\
│   └── webhook.py          

### Setup Instructions

1. Clone the Repository:
```
git clone https://github.com/yourusername/self-healing-infra.git
cd self-healing-infra
```

2. Install Dependencies:Update system and install tools:
```
sudo apt update && sudo apt upgrade -y
sudo apt install nginx python3-pip ansible -y
pip3 install flask
```
Install Prometheus, Alertmanager, Node Exporter, and NGINX Prometheus Exporter (see detailed steps in the project report).

3. Configure Services:

- Copy configs to appropriate paths:
```
sudo mkdir -p /opt/{prometheus,alertmanager,ansible,webhook}
sudo cp prometheus/* /opt/prometheus/
sudo cp alertmanager/* /opt/alertmanager/
sudo cp ansible/* /opt/ansible/
sudo cp webhook/* /opt/webhook/
```

- Set up systemd services for Prometheus, Alertmanager, Node Exporter, and NGINX Exporter (refer to report for service files).
- Enable NGINX stub_status:Edit /etc/nginx/sites-enabled/default, add:
```
location /stub_status {
    stub_status;
}
```
Restart NGINX: sudo systemctl restart nginx.

4. Start Services:
```
sudo systemctl start prometheus alertmanager node_exporter nginx-exporter
sudo systemctl enable prometheus alertmanager node_exporter nginx-exporter
python3 /opt/webhook/webhook.py &
```

5. Test the Setup:

- Access Prometheus UI: http://localhost:9090
- Access Alertmanager UI: http://localhost:9093
- Simulate failure: sudo systemctl stop nginx or stress CPU with stress --cpu 8 (install: sudo apt install stress -y).
- Check alerts in Prometheus/Alermanager UIs and verify NGINX restarts via logs (journalctl -u nginx).



### Demo

- Logs: Check webhook logs (/opt/webhook/webhook.py output) and Ansible logs (ansible-playbook /opt/ansible/recover.yml).
- Screenshots: Add to screenshots/ folder. Example: Prometheus Alerts page (http://localhost:9090/alerts) showing "NginxDown" firing, NGINX status before/after recovery.
- Sample log:
```
[Alertmanager] level=info msg="Sending webhook" url=http://localhost:5000/webhook
[Webhook] {
    "receiver": "ansible-webhook",
    "status": "firing",
    "alerts": [{ "labels": { "alertname": "NginxDown" } }]
}
[Ansible] TASK [Restart NGINX] changed: [localhost]
```


### Usage

- Monitor NGINX and CPU via Prometheus.
- Alerts trigger automatically on failure.
- Ansible playbook (recover.yml) restarts NGINX or (optionally) reboots the system.
- Customize thresholds in prometheus/rules.yml or recovery actions in ansible/recover.yml.

### Notes

- Ensure ports 9090, 9093, 9100, 9113, and 5000 are open (sudo ufw allow 9090,9093,9100,9113,5000).
- For Docker, adapt to docker-compose.yml (not included but can be derived from setup).
- The LaTeX report (docs/self_healing_report.tex) can be compiled to PDF with pdflatex self_healing_report.tex.

### Contributing

- Fork the repo, make changes, and submit a pull request.
- Report issues via GitHub Issues.

### License
MIT License (add LICENSE file if needed).
