import feedparser
import smtplib
import os
from email.mime.text import MIMEText
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

QUERY = "computación OR tecnología OR software"
FEED_URL = f"https://news.google.com/rss/search?q={quote(QUERY)}+when:1d&hl=es-419&gl=MX&ceid=MX:es-419"
def obtener_noticias():
    feed = feedparser.parse(FEED_URL)
    noticias = []
    for entrada in feed.entries[:10]:
        noticias.append(f"• {entrada.title}\n  {entrada.link}")
    return noticias

def armar_correo(noticias):
    fecha = datetime.now().strftime("%d/%m/%Y")
    cuerpo = f"Noticias de computación en México — {fecha}\n\n"
    cuerpo += "\n\n".join(noticias) if noticias else "No se encontraron noticias nuevas hoy."
    return cuerpo

def enviar_correo(cuerpo):
    remitente = os.environ["EMAIL_FROM"]
    password = os.environ["EMAIL_APP_PASSWORD"]
    destinatario = os.environ["EMAIL_TO"]

    msg = MIMEText(cuerpo)
    msg["Subject"] = "📰 Noticias de computación en México"
    msg["From"] = remitente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, msg.as_string())

if __name__ == "__main__":
    noticias = obtener_noticias()
    cuerpo = armar_correo(noticias)
    enviar_correo(cuerpo)
    print("Correo enviado con", len(noticias), "noticias.")
