import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import parseaddr
from typing import List

from config.settings import settings
from utils.logger import get_logger

logger = get_logger("smtp-client")

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _sanitize_header(value: str) -> str:
    """Strip CR/LF to prevent header injection."""
    return value.replace("\r", "").replace("\n", "")


def _validate_recipients(recipients: List[str]) -> List[str]:
    """Return only well-formed addresses; log and drop invalid ones."""
    clean = []
    for raw in recipients:
        _, addr = parseaddr(raw)
        if addr and _EMAIL_RE.match(addr):
            clean.append(addr)
        else:
            logger.warning(f"Dropped invalid recipient address")
    return clean


class SMTPClient:
    def __init__(self):
        self.host = settings.smtp_host
        self.port = settings.smtp_port
        self.user = settings.smtp_user
        self.password = settings.smtp_password

    def send(
        self,
        subject: str,
        recipients: List[str],
        html_body: str,
        text_body: str = "",
    ) -> bool:
        safe_recipients = _validate_recipients(recipients)
        if not safe_recipients:
            logger.error("Send aborted — no valid recipients after validation")
            return False

        safe_subject = _sanitize_header(subject)

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = safe_subject
            msg["From"] = _sanitize_header(self.user)
            msg["To"] = ", ".join(safe_recipients)

            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(self.host, self.port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, safe_recipients, msg.as_string())

            logger.info(f"SENT | recipients={len(safe_recipients)}")
            return True

        except Exception as e:
            logger.error(f"SMTP send failed | error_type={type(e).__name__}")
            return False


smtp_client = SMTPClient()
