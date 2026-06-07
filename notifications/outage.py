import json
from datetime import datetime
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader

from config.settings import settings
from utils.logger import get_logger
from utils.smtp_client import smtp_client

logger = get_logger("outage")

_SEVERITY_IMPACT = {"P1": "Critical", "P2": "High", "P3": "Medium"}


def _load_recipients(group: str) -> List[str]:
    with open("config/recipients.json") as f:
        groups = json.load(f)
    return groups.get(group, [])


def send_outage_notification(
    incident_id: str,
    severity: str,
    affected_system: str,
    impact: str,
    status: str,
    start_time: str,
    eta: str,
    current_status: str,
    workaround: str = "",
    incident_commander: str = "",
    recipient_group: Optional[str] = None,
    additional_recipients: Optional[List[str]] = None,
) -> bool:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("outage.html")

    severity_label = f"{severity} — {_SEVERITY_IMPACT.get(severity, 'Unknown')}"
    html_body = template.render(
        incident_id=incident_id,
        severity=severity,
        severity_label=severity_label,
        affected_system=affected_system,
        impact=impact,
        status=status,
        start_time=start_time,
        eta=eta,
        current_status=current_status,
        workaround=workaround,
        incident_commander=incident_commander,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    impact_label = _SEVERITY_IMPACT.get(severity, "Unknown")
    subject = f"[{severity} OUTAGE] {affected_system} — Impact: {impact_label} | ETA: {eta}"

    recipients = _load_recipients(recipient_group or settings.default_group)
    if additional_recipients:
        recipients = list(set(recipients + additional_recipients))

    if not recipients:
        logger.warning("No recipients — outage notification aborted")
        return False

    logger.info(f"Outage notification | {incident_id} | {severity} | {affected_system}")
    return smtp_client.send(subject, recipients, html_body)
