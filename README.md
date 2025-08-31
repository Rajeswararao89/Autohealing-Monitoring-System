## 🛠️ Self-Healing Infrastructure with Prometheus, Alertmanager, Grafana & Ansible
## 📌 Project Overview

- This project demonstrates a self-healing monitoring system that automatically detects service failures (e.g., Nginx, MySQL) and recovers them without manual intervention.

- Prometheus → Scrapes metrics from services & exporters
- Alertmanager → Triggers alerts on defined conditions
- Webhook (Flask App) → Receives alerts and triggers automation
- Ansible → Executes playbooks to restart failed services
- Grafana → Provides real-time visualization & dashboards

## ✅ With this setup, critical services are monitored, alerted, and auto-healed seamlessly.

## 🚀 Features

- 📊 Service Monitoring – Nginx, MySQL, Node Exporter, Blackbox Exporter
- 🔔 Alerting System – Prometheus Alertmanager rules for availability & health
- 🤖 Self-Healing Automation – Automatic restart of failed services using Ansible
- 📈 Visualization – Grafana dashboards for metrics & alert visualization
- ⚡ Extensible – Can be expanded to monitor any critical service (Apache, Redis, Docker, etc.)
  
## 🏗️ Architecture

## 📂 Project Structure
- ├── ansible/
- │   ├── playbooks/
- │   │   ├── restart_nginx.yml
- │   │   └── restart_mysql.yml
- ├── prometheus/
- │   ├── prometheus.yml
- │   ├── alert.rules.yml
- ├── webhook/
- │   ├── app.py
- │   └── requirements.txt
- ├── grafana/
- │   └── dashboards/   # JSON files for imported dashboards
- └── README.md

## ⚙️ Setup Instructions
## 1️⃣ Install Prometheus & Exporters

- Install Prometheus, Node Exporter, Blackbox Exporter, MySQL Exporter
- Configure prometheus.yml with targets
  
## 2️⃣ Configure Alert Rules

- Example (alert.rules.yml):

- groups:
  - name: nginx-availability
    rules:
      - alert: NginxDown
        expr: probe_success{instance="http://localhost:80"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "NGINX is unreachable"
          description: "HTTP probe failed for {{ $labels.instance }} for >1m"

## 3️⃣ Setup Alertmanager

- alertmanager.yml

- route:
   group_by: ['alertname']
  receiver: 'web.hook'

- receivers:
   - name: 'web.hook'
     webhook_configs:
      - url: 'http://127.0.0.1:5001/alert'

## 4️⃣ Deploy Webhook (Flask App)

- webhook/app.py

- @app.route('/alert', methods=['POST'])
- def alert():
    data = request.json
    if "NginxDown" in str(data):
        run_ansible_playbook("restart_nginx.yml")
    elif "MySQLDown" in str(data):
        run_ansible_playbook("restart_mysql.yml")

## 5️⃣ Self-Healing with Ansible

- Example playbook:

- name: Restart NGINX if down
  hosts: localhost
  tasks:
    - name: Restart NGINX
      service:
        name: nginx
        state: restarted

## 6️⃣ Grafana Setup

- Import dashboards (Node Exporter, MySQL, Blackbox, Prometheus)
- Create custom panels for alerts


## 🌟 Key Outcomes

- Achieved Zero Downtime Recovery for monitored services
- Implemented End-to-End Monitoring → Alerting → Auto-Healing pipeline
- Enhanced Reliability & Resilience of infrastructure

## 📖 Future Improvements

- Add support for Docker, Redis, Apache auto-healing
- Deploy on Kubernetes with Prometheus Operator
- Integrate with Slack/Email alerts for visibility

## 👨‍💻 Author
- Rajeswara Rao

- 🚀 DevOps Enthusiast | Cloud | CI/CD | Monitoring & Automation
Rajeswara Rao

🚀 DevOps Enthusiast | Cloud | CI/CD | Monitoring & Automation
