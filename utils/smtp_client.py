import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from config.settings import settings
from utils.logger import get_logger

logger = get_logger("smtp-client")


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
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.user
            msg["To"] = ", ".join(recipients)

            if text_body:
                msg.attach(MIMEText(text_body, "plain"))
            msg.attach(MIMEText(html_body, "html"))

            with smtplib.SMTP(self.host, self.port) as server:
                server.ehlo()
                server.starttls()
                server.login(self.user, self.password)
                server.sendmail(self.user, recipients, msg.as_string())

            logger.info(
                f"SENT | Subject: {subject} | To: {recipients}"
            )
            return True

        except Exception as e:
            logger.error(
                f"FAILED | Subject: {subject} | Error: {e}"
            )
            return False


smtp_client = SMTPClient()
