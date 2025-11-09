from fastapi import APIRouter, HTTPException
from model.predict import predict_spam
import imaplib, email
from email.header import decode_header
import os
import datetime
from dotenv import load_dotenv

router = APIRouter()
load_dotenv()  # Carga variables desde .env

def connect_to_mail(server, username, password, folder="INBOX"):
    imaplib._MAXLINE = 10000  # Por si hay líneas largas
    mail = imaplib.IMAP4_SSL(server)
    mail._encoding = "utf-8"  # Fuerza codificación UTF-8
    mail.login(username, password)
    mail.select(folder)
    return mail

def fetch_emails(mail, limit=50):
    # Limita la búsqueda a los últimos 30 días
    today = datetime.date.today()
    since = (today - datetime.timedelta(days=30)).strftime("%d-%b-%Y")
    status, messages = mail.search(None, f'SINCE {since}')
    
    if status != "OK":
        raise HTTPException(status_code=500, detail="No se pudieron recuperar los correos.")

    email_ids = messages[0].split()[-limit:]
    results = []

    for eid in email_ids:
        _, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        subject, encoding = decode_header(msg.get("Subject"))[0]
        subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
        sender = msg.get("From")

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    charset = part.get_content_charset() or "utf-8"
                    body = part.get_payload(decode=True).decode(charset, errors="ignore")
                    break
        else:
            charset = msg.get_content_charset() or "utf-8"
            body = msg.get_payload(decode=True).decode(charset, errors="ignore")

        full_text = f"{subject}\n{body}".strip()
        result = predict_spam(full_text)

        results.append({
            "from": sender,
            "subject": subject,
            "is_spam": result["is_spam"],
            "confidence": result["confidence"],
            "cleaned_text": result["cleaned_text"]
        })

    return results

@router.get("/scan-emails")
def scan_emails():
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(status_code=500, detail="Credenciales de correo no configuradas.")

    try:
        mail = connect_to_mail("imap.gmail.com", EMAIL_USER, EMAIL_PASS)
        return fetch_emails(mail)
    except Exception as e:
        print("❌ ERROR IMAP:", str(e))  # Diagnóstico en consola
        raise HTTPException(status_code=500, detail=f"Error al conectar con el servidor de correo: {str(e)}")