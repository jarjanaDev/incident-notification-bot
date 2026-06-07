import json
from datetime import datetime
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader

from config.settings import settings
from utils.logger import get_logger
from utils.smtp_client import smtp_client

logger = get_logger("resolution")


def _load_recipients(group: str) -> List[str]:
    with open("config/recipients.json") as f:
        groups = json.load(f)
    return groups.get(group, [])


def send_resolution_notification(
    incident_id: str,
    affected_system: str,
    resolved_at: str,
    duration: str,
    root_cause: str,
    resolution_summary: str,
    severity: str = "P2",
    incident_commander: str = "",
    follow_up_actions: str = "",
    recipient_group: Optional[str] = None,
    additional_recipients: Optional[List[str]] = None,
) -> bool:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("resolution.html")

    html_body = template.render(
        incident_id=incident_id,
        affected_system=affected_system,
        resolved_at=resolved_at,
        duration=duration,
        root_cause=root_cause,
        resolution_summary=resolution_summary,
        severity=severity,
        incident_commander=incident_commander,
        follow_up_actions=follow_up_actions,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    subject = f"[RESOLVED] {affected_system} — {incident_id} | Duration: {duration}"

    recipients = _load_recipients(recipient_group or settings.default_group)
    if additional_recipients:
        recipients = list(set(recipients + additional_recipients))

    if not recipients:
        logger.warning("No recipients — resolution notification aborted")
        return False

    logger.info(f"Resolution notification | {incident_id} | {affected_system} | Resolved at {resolved_at}")
    return smtp_client.send(subject, recipients, html_body)
