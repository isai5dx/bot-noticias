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
    return feed.entries[:10]

def armar_correo_html(noticias):
    fecha = datetime.now().strftime("%d de %B, %Y")

    tarjetas = ""
    for n in noticias:
        fuente = n.get("source", {}).get("title", "")
        tarjetas += f"""
        <tr>
          <td style="padding: 16px 0; border-bottom: 1px solid #e5e5e5;">
            <a href="{n.link}" style="font-size: 16px; font-weight: 600; color: #1a1a1a; text-decoration: none; line-height: 1.4;">
              {n.title}
            </a>
            <div style="font-size: 13px; color: #888; margin-top: 6px;">{fuente}</div>
          </td>
        </tr>
        """

    if not noticias:
        tarjetas = """
        <tr><td style="padding: 24px 0; color: #666;">No se encontraron noticias nuevas hoy.</td></tr>
        """

    html = f"""
    <html>
    <body style="margin:0; padding:0; background-color:#f4f4f4; font-family: -apple-system, Arial, sans-serif;">
      <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f4; padding: 24px 0;">
        <tr>
          <td align="center">
            <table width="600" cellpadding="0" cellspacing="0" style="background-color:#ffffff; border-radius: 10px; overflow: hidden;">
              <tr>
                <td style="background-color:#1a1a2e; padding: 24px 32px;">
                  <div style="color:#ffffff; font-size: 20px; font-weight: 700;">💻 Noticias de computación en México</div>
                  <div style="color:#a0a0c0; font-size: 13px; margin-top: 4px;">{fecha}</div>
                </td>
              </tr>
              <tr>
                <td style="padding: 8px 32px 24px 32px;">
                  <table width="100%" cellpadding="0" cellspacing="0">
                    {tarjetas}
                  </table>
                </td>
              </tr>
              <tr>
                <td style="background-color:#fafafa; padding: 16px 32px; text-align:center;">
                  <span style="font-size: 12px; color: #999;">Generado automáticamente todos los días a las 7am</span>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </body>
    </html>
    """
    return html

def enviar_correo(cuerpo_html):
    remitente = os.environ["EMAIL_FROM"]
    password = os.environ["EMAIL_APP_PASSWORD"]
    destinatario = os.environ["EMAIL_TO"]

    msg = MIMEText(cuerpo_html, "html")
    msg["Subject"] = "📰 Noticias de computación en México"
    msg["From"] = remitente
    msg["To"] = destinatario

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as servidor:
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, msg.as_string())

if __name__ == "__main__":
    noticias = obtener_noticias()
    cuerpo = armar_correo_html(noticias)
    enviar_correo(cuerpo)
    print("Correo enviado con", len(noticias), "noticias.")