# 🔔 Incident Notification Bot

> Automated IT incident and maintenance notification system — eliminates manual communication during outages.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![SMTP](https://img.shields.io/badge/SMTP-Email-EA4335?style=flat-square&logo=gmail&logoColor=white)
![REST API](https://img.shields.io/badge/REST-API-009688?style=flat-square)
![ITIL](https://img.shields.io/badge/ITIL-Compliant-purple?style=flat-square)

---

## 🧩 Problem It Solves

During IT incidents and maintenance windows, operations teams manually compose and send notification emails to stakeholders — a slow, error-prone process that delays communication and wastes engineer time during high-pressure situations.

**This tool automates the entire notification workflow:**
- Generates structured, professional notifications instantly
- Sends to configured stakeholder groups via SMTP
- Supports outage alerts, maintenance windows, and resolution notices
- Logs all notifications with timestamps for audit trail

---

## ⚙️ Features

- ✅ **Outage Notifications** — P1/P2/P3 incident alerts with impact, ETA, and workaround
- ✅ **Maintenance Windows** — Scheduled downtime notices with affected systems
- ✅ **Resolution Notices** — Closure notifications with RCA summary
- ✅ **Stakeholder Groups** — Configurable recipient lists per application/team
- ✅ **Templates** — ITIL-aligned notification templates
- ✅ **Audit Log** — All notifications logged with sender, recipients, timestamp
- ✅ **REST API Mode** — Trigger notifications via API call from monitoring tools

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| Email | SMTP (smtplib) + HTML templates |
| API | FastAPI (optional REST trigger) |
| Config | Pydantic Settings + .env |
| Logging | Python logging + rotating file handler |

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/jarjanaDev/incident-notification-bot
cd incident-notification-bot

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your SMTP settings and recipient lists

# Run
python main.py
```

---

## 📁 Project Structure

```
incident-notification-bot/
├── main.py                  # Entry point
├── config/
│   ├── settings.py          # Pydantic config
│   └── recipients.json      # Stakeholder groups
├── notifications/
│   ├── outage.py            # Outage notification logic
│   ├── maintenance.py       # Maintenance window logic
│   └── resolution.py        # Resolution/closure logic
├── templates/
│   ├── outage.html          # Email HTML template
│   ├── maintenance.html
│   └── resolution.html
├── utils/
│   ├── smtp_client.py       # SMTP handler
│   └── logger.py            # Audit logging
├── api/
│   └── routes.py            # FastAPI REST trigger (optional)
├── .env.example
├── requirements.txt
└── README.md
```

---

## 📧 Sample Notification Output

```
Subject: [P1 OUTAGE] Payment Service Degradation — Impact: High | ETA: 14:30 IST

Dear Stakeholders,

INCIDENT SUMMARY
─────────────────────────────────────
Incident ID  : INC0043821
Severity     : P1 — Critical
Status       : ACTIVE — Under Investigation
Affected     : Payment Processing Service
Impact       : Users unable to complete transactions
Start Time   : 13:45 IST
ETA          : 14:30 IST

CURRENT STATUS
Investigation ongoing. Payment team and infra team engaged.
Workaround: Manual processing via backup channel.

Next update in: 30 minutes
─────────────────────────────────────
Incident Commander: Santosh Dharma
```

---

## 🔧 Configuration

```env
# .env
SMTP_HOST=smtp.office365.com
SMTP_PORT=587
SMTP_USER=notifications@company.com
SMTP_PASSWORD=your_password

# Recipient groups (configured in recipients.json)
DEFAULT_GROUP=it-team
ESCALATION_GROUP=management
```

---

## 📌 Use Cases

- IT Operations teams managing multiple applications
- NOC (Network Operations Center) incident communication
- Any team that sends repetitive structured notifications during incidents

---

## 👤 Author

**Santosh Dharma Jarjana**
[LinkedIn](https://linkedin.com/in/dharmasantosh0007) · [GitHub](https://github.com/jarjanaDev)
