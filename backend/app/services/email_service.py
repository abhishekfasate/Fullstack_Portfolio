"""Email service — sends contact-form notifications via SMTP."""

import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def _build_html(name: str, email: str, subject: str, message: str) -> str:
    return f"""
    <html><body style="font-family:sans-serif;max-width:600px;margin:auto">
      <h2 style="color:#2563eb">New Portfolio Contact</h2>
      <table>
        <tr><td><b>From:</b></td><td>{name} ({email})</td></tr>
        <tr><td><b>Subject:</b></td><td>{subject}</td></tr>
      </table>
      <hr/>
      <p>{message.replace(chr(10), '<br/>')}</p>
      <hr/>
      <small style="color:#6b7280">Sent via your portfolio contact form</small>
    </body></html>
    """


async def send_contact_email(name: str, email: str, subject: str, message: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Portfolio] {subject}"
    msg["From"] = settings.MAIL_FROM
    msg["To"] = settings.MAIL_TO
    msg["Reply-To"] = email

    msg.attach(MIMEText(f"From: {name} ({email})\n\n{message}", "plain"))
    msg.attach(MIMEText(_build_html(name, email, subject, message), "html"))

    raw = msg.as_string()

    def _send() -> None:
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_FROM, settings.MAIL_TO, raw)

    await asyncio.to_thread(_send)


async def send_auto_reply(name: str, email: str) -> None:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Thanks for reaching out!"
    msg["From"] = settings.MAIL_FROM
    msg["To"] = email

    body = (
        f"Hi {name},\n\nThanks for your message! "
        "I'll get back to you as soon as possible.\n\nBest,\nAbhishek"
    )
    msg.attach(MIMEText(body, "plain"))

    raw = msg.as_string()

    def _send() -> None:
        with smtplib.SMTP(settings.MAIL_SERVER, settings.MAIL_PORT) as server:
            server.starttls()
            server.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
            server.sendmail(settings.MAIL_FROM, email, raw)

    await asyncio.to_thread(_send)