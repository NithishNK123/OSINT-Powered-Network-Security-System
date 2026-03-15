<div align="center">
  <h1>🛡️ OSINT-Powered Network Security System</h1>
  <p><strong>An Enterprise-Grade, AI-Driven Security Operations Center (SOC) Dashboard</strong></p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python 3.8+">
    <img src="https://img.shields.io/badge/Flask-3.0.3-black.svg?logo=flask" alt="Flask">
    <img src="https://img.shields.io/badge/React-18-blue.svg?logo=react" alt="React">
    <img src="https://img.shields.io/badge/Status-Production_Ready-success.svg" alt="Status">
    <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  </p>
</div>

---

## 📖 Overview

The **OSINT-Powered Network Security System** is a comprehensive, production-ready Security Operations Center (SOC) intelligence platform. It seamlessly merges **Open Source Intelligence (OSINT)** gathering with **AI-driven threat analysis**, providing security analysts with real-time, actionable insights into network vulnerabilities, malicious IPs, and domain reputations.

Built with a highly responsive, glassmorphic UI, robust Role-Based Access Control (RBAC), and automated alerting pipelines, this project demonstrates full-stack engineering, secure backend architecture, and modern cybersecurity practices.

---

## ✨ Key Features

- 🔍 **Real-Time OSINT Integration**: Automated threat intelligence gathering using APIs from **VirusTotal**, **AbuseIPDB**, **Shodan**, and **AlienVault OTX**.
- 🤖 **AI-Powered Threat Engine**: Behavioral analysis and intelligent scoring system to categorize and prioritize critical threats dynamically.
- 🛡️ **Role-Based Access Control (RBAC)**: Secure, multi-tier access system featuring separate privileges for **Viewers**, **Analysts**, and **Admins**.
- 📊 **Modern SOC Dashboard**: A stunning, responsive UI featuring real-time data visualization (Chart.js), dark/light mode toggle with custom animations, and a premium glassmorphic aesthetic.
- 🔔 **Automated Webhook Alerting**: Built-in Slack/Discord webhook integrations for instant notification of High and Critical risk alerts.
- 📑 **Comprehensive Reporting**: Generate detailed PDF and Excel forensic reports for compliance and auditing.

---

## 🛠️ Technology Stack

**Backend Engine**
- Python 3.8+
- Flask (Web Framework)
- SQLite (Lightweight Relational Database)
- Custom RBAC Middleware & Session Management

**Frontend & UI**
- HTML5, Jinja2, Vanilla JS
- Custom CSS Properties with smooth cinematic transitions (Tailwind/Vite available in isolated frontend module)
- Chart.js (Interactive data visualization)
- FontAwesome 6 (Enterprise iconography)

**Security & Integrations**
- External OSINT APIs (VirusTotal, Shodan, AbuseIPDB, Censys, GreyNoise)
- Secure Password Hashing & Environment Configurations

---

## 🎯 Architecture & Structure

The codebase is divided into clear, modular components designed for scalability:

```text
OSINT-Powered-Network-Security-System/
├── Update_1_OSINT/
│   ├── core/              # AI Engine, Threat Engine, Rule Correlation, RBAC
│   ├── dashboard/         # Flask application, routing, and Jinja2 templates
│   │   ├── static/        # Modern CSS theme system, Chart.js logic
│   │   └── templates/     # 8+ HTML views (Analyze, Dashboard, Settings, etc.)
│   ├── scripts/           # Standalone OSINT data collectors (Shodan, VT, etc.)
│   ├── config/            # Settings, configurations, and API keys
│   └── data/              # SQLite database and log storage
└── frontend/              # Alternative React + Vite UI implementation
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/NithishNK123/OSINT-Powered-Network-Security-System.git
cd OSINT-Powered-Network-Security-System
```

### 2. Install Dependencies
Navigate to the core engine directory and install the required Python packages:
```bash
cd Update_1_OSINT
pip install -r requirements.txt
```

### 3. Configure API Keys
Add your OSINT API keys to the configuration block in `Update_1_OSINT/config/api_keys.py` to enable live threat data gathering.

### 4. Run the Platform
Start the Flask application:
```bash
python dashboard/app.py
```
*The application will be hosted locally at `http://127.0.0.1:5000`*

### 5. Access the Dashboard
Navigate to your localhost port in any modern browser. You can test the platform using the built-in demo credentials for the different RBAC roles (Viewer, Analyst, Admin).

---

## 📈 Platform Preview

### Performance & Quality Metrics
- **Load Times:** Dashboard, Analysis, and History pages all load in under 1 second.
- **Security:** CSRF-protection ready, secure server-side session cookies, complete RBAC perimeter.
- **Accessibility:** WCAG AA color contrast compliant, comprehensive responsive layouts for Mobile, Tablet, and Desktop.

---

## 📝 License
This project is open-source and available under the terms of the MIT License.