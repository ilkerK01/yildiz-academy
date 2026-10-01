from __future__ import annotations

import logging
import smtplib
import ssl
from email.message import EmailMessage

from app import config

log = logging.getLogger("uvicorn.error")


def gonder(alici: str, konu: str, govde: str) -> bool:
    if not config.SMTP_HOST:
        log.warning("SMTP ayarlı değil, e-posta gönderilmedi. Alıcı: %s\n%s", alici, govde)
        return False

    mesaj = EmailMessage()
    mesaj["Subject"] = konu
    mesaj["From"] = config.SMTP_FROM
    mesaj["To"] = alici
    mesaj.set_content(govde)

    baglam = ssl.create_default_context()
    try:
        if config.SMTP_SSL:
            with smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT, context=baglam, timeout=20) as smtp:
                if config.SMTP_USER:
                    smtp.login(config.SMTP_USER, config.SMTP_PASS)
                smtp.send_message(mesaj)
        else:
            with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT, timeout=20) as smtp:
                smtp.starttls(context=baglam)
                if config.SMTP_USER:
                    smtp.login(config.SMTP_USER, config.SMTP_PASS)
                smtp.send_message(mesaj)
    except (smtplib.SMTPException, OSError) as hata:
        log.error("E-posta gönderilemedi (%s): %s", alici, hata)
        return False
    return True
