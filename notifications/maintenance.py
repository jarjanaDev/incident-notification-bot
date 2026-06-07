import json
from datetime import datetime
from typing import List, Optional

from jinja2 import Environment, FileSystemLoader

from config.settings import settings
from utils.logger import get_logger
from utils.smtp_client import smtp_client

logger = get_logger("maintenance")


def _load_recipients(group: str) -> List[str]:
    with open("config/recipients.json") as f:
        groups = json.load(f)
    return groups.get(group, [])


def send_maintenance_notification(
    maintenance_id: str,
    affected_systems: List[str],
    scheduled_start: str,
    scheduled_end: str,
    description: str,
    impact: str,
    lead_engineer: str = "",
    rollback_plan: str = "",
    recipient_group: Optional[str] = None,
    additional_recipients: Optional[List[str]] = None,
) -> bool:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("maintenance.html")

    html_body = template.render(
        maintenance_id=maintenance_id,
        affected_systems=affected_systems,
        scheduled_start=scheduled_start,
        scheduled_end=scheduled_end,
        description=description,
        impact=impact,
        lead_engineer=lead_engineer,
        rollback_plan=rollback_plan,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    systems_str = ", ".join(affected_systems)
    subject = f"[MAINTENANCE] {systems_str} | {scheduled_start} — {scheduled_end}"

    recipients = _load_recipients(recipient_group or settings.default_group)
    if additional_recipients:
        recipients = list(set(recipients + additional_recipients))

    if not recipients:
        logger.warning("No recipients — maintenance notification aborted")
        return False

    logger.info(f"Maintenance notification | {maintenance_id} | Systems: {systems_str}")
    return smtp_client.send(subject, recipients, html_body)
