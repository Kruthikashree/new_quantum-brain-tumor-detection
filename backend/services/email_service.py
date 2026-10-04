import os, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email(to, subject, body, attachment=None, filename="report.pdf"):
    # Brevo/other SMTP if configured, otherwise Gmail
    host = os.getenv("SMTP_HOST")
    if host:
        port = int(os.getenv("SMTP_PORT", "587"))
        user = os.getenv("SMTP_USER")
        password = os.getenv("SMTP_PASSWORD")
        sender = os.getenv("MAIL_FROM") or user
        use_ssl = False
    else:
        host, port, use_ssl = "smtp.gmail.com", 465, True
        user = os.getenv("MAIL_USER")
        password = os.getenv("MAIL_APP_PASSWORD")
        sender = user

    if not (user and password):
        print("\n===== EMAIL (dev mode, not sent) =====")
        print("To:", to)
        print("Subject:", subject)
        print(body)
        print("======================================\n")
        return

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    if attachment:
        msg.add_attachment(attachment, maintype="application",
                           subtype="pdf", filename=filename)

    if use_ssl:
        with smtplib.SMTP_SSL(host, port) as s:
            s.login(user, password)
            s.send_message(msg)
    else:
        with smtplib.SMTP(host, port) as s:
            s.starttls()
            s.login(user, password)
            s.send_message(msg)