import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ==========================================
# CONFIGURACIÓN DEL SERVICIO
# ==========================================
SENDER_EMAIL = "diego.1202@yahoo.com"
RECIPIENT_EMAIL = "diego.1202@yahoo.com"
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 465

YAHOO_APP_PASSWORD = os.environ.get("YAHOO_APP_PASSWORD", "").strip()

# ==========================================
# PLANTILLA HTML DE ALTO CONTRASTE
# ==========================================
def generate_email_html():
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FlyCoral - Alerta de Vuelos</title>
</head>
<body style="margin: 0; padding: 24px; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #e2e8f0;">
  
  <!-- Contenedor Principal -->
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 680px; background-color: #131b2e; border-radius: 14px; border: 1px solid #2d3748; overflow: hidden;">
    
    <!-- Header -->
    <tr>
      <td style="padding: 24px 28px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-bottom: 2px solid #38bdf8;">
        <table width="100%" border="0" cellpadding="0" cellspacing="0">
          <tr>
            <td>
              <span style="font-size: 24px; font-weight: 800; letter-spacing: -0.5px; color: #ffffff;">FlyCoral</span>
              <span style="margin-left: 8px; font-size: 11px; font-weight: 700; background-color: #0284c7; color: #ffffff; padding: 3px 8px; border-radius: 6px; text-transform: uppercase;">AR</span>
              <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Asistente Experta en Tarifas y Rutas</div>
            </td>
          </tr>
        </table>
      </td>
    </tr>

    <!-- Contenido -->
    <tr>
      <td style="padding: 28px;">
        
        <!-- Badge Alerta -->
        <div style="display: inline-block; padding: 6px 12px; background-color: rgba(56, 189, 248, 0.12); border: 1px solid #0284c7; border-radius: 20px; font-size: 12px; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 16px;">
          ✈ Alerta Programada de Vuelo
        </div>

        <!-- Título de la Ruta -->
        <h1 style="font-size: 20px; font-weight: 700; color: #f8fafc; margin: 0 0 12px 0;">
          Buenos Aires (EZE) <span style="color: #38bdf8;">➔</span> Madrid (MAD)
        </h1>

        <p style="font-size: 14px; line-height: 1.6; color: #cbd5e1; margin: 0 0 24px 0;">
          Hola, acá estuve monitoreando las alternativas para esta ruta y consolidé las opciones más convenientes según tu alerta:
        </p>

        <!-- Tabla de Vuelos (Alto Contraste) -->
        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; border: 1px solid #334155; border-radius: 8px; overflow: hidden; margin-bottom: 24px;">
          <thead>
            <tr style="background-color: #1e293b;">
              <th align="left" style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; border-bottom: 1px solid #334155;">Opción</th>
              <th align="left" style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; border-bottom: 1px solid #334155;">Fechas</th>
              <th align="left" style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; border-bottom: 1px solid #334155;">Aerolínea / Escala</th>
              <th align="left" style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; border-bottom: 1px solid #334155;">Tarifa</th>
              <th align="center" style="padding: 12px 14px; font-size: 12px; font-weight: 700; color: #94a3b8; text-transform: uppercase; border-bottom: 1px solid #334155;">Acción</th>
            </tr>
          </thead>
          <tbody>
            <!-- Fila 1: Directo -->
            <tr style="background-color: #0f172a; border-bottom: 1px solid #1e293b;">
              <td style="padding: 14px; font-size: 13px; font-weight: 700; color: #f8fafc;">
                Directo
              </td>
              <td style="padding: 14px; font-size: 13px; color: #e2e8f0;">
                15 Oct ➔ 23 Oct
              </td>
              <td style="padding: 14px; font-size: 13px; color: #cbd5e1;">
                <strong>Iberia / Level</strong><br>
                <span style="font-size: 11px; color: #94a3b8;">22:45 EZE ➔ 14:35 MAD</span>
              </td>
              <td style="padding: 14px; font-size: 13px; font-weight: 700; color: #38bdf8;">
                USD 880<br>
                <span style="font-size: 11px; font-weight: normal; color: #94a3b8;">ARS 1.280.000</span>
              </td>
              <td align="center" style="padding: 14px;">
                <a href="https://www.google.com/travel/flights" target="_blank" style="display: inline-block; background-color: #0284c7; color: #ffffff; font-size: 12px; font-weight: 700; text-decoration: none; padding: 8px 14px; border-radius: 6px;">
                  Ver Vuelo
                </a>
              </td>
            </tr>

            <!-- Fila 2: 1 Escala (Mejor Precio) -->
            <tr style="background-color: #131b2e;">
              <td style="padding: 14px; font-size: 13px; font-weight: 700; color: #34d399;">
                1 Escala ★
              </td>
              <td style="padding: 14px; font-size: 13px; color: #e2e8f0;">
                15 Oct ➔ 23 Oct
              </td>
              <td style="padding: 14px; font-size: 13px; color: #cbd5e1;">
                <strong>Air Europa</strong><br>
                <span style="font-size: 11px; color: #94a3b8;">13:20 EZE ➔ 09:15 MAD</span>
              </td>
              <td style="padding: 14px; font-size: 13px; font-weight: 700; color: #34d399;">
                USD 740<br>
                <span style="font-size: 11px; font-weight: normal; color: #94a3b8;">ARS 1.080.000</span>
              </td>
              <td align="center" style="padding: 14px;">
                <a href="https://www.google.com/travel/flights" target="_blank" style="display: inline-block; background-color: #059669; color: #ffffff; font-size: 12px; font-weight: 700; text-decoration: none; padding: 8px 14px; border-radius: 6px;">
                  Ver Vuelo
                </a>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Tarjeta de Veredicto de Coral -->
        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #1e293b; border-left: 4px solid #38bdf8; border-radius: 0 8px 8px 0; margin-bottom: 24px;">
          <tr>
            <td style="padding: 16px 20px;">
              <div style="font-size: 13px; font-weight: 800; text-transform: uppercase; color: #38bdf8; letter-spacing: 0.5px; margin-bottom: 6px;">
                💡 Veredicto de Coral
              </div>
              <div style="font-size: 13px; line-height: 1.5; color: #f1f5f9; font-style: italic;">
                "USD 740 para cruzar el charco es una tarifa excelente; con esa escala corta te ahorrás unos cuantos dólares para gastar en destino."
              </div>
            </td>
          </tr>
        </table>

        <!-- Footer / Firma -->
        <p style="font-size: 12px; color: #64748b; line-height: 1.5; margin: 0; border-top: 1px solid #1e293b; padding-top: 16px;">
          Este reporte fue generado y despachado de forma automática por tu bot <strong>FlyCoral</strong> a través de tu cuenta <code>diego.1202@yahoo.com</code>.
        </p>

      </td>
    </tr>
  </table>

</body>
</html>
"""

# ==========================================
# ENVÍO DEL CORREO MEDIANTE SMTP
# ==========================================
def send_flight_alert():
    if not YAHOO_APP_PASSWORD:
        print("ERROR: No se configuró el secreto YAHOO_APP_PASSWORD.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "✈ FlyCoral: Oportunidad de Vuelo EZE ➔ MAD (USD 740)"
    msg["From"] = f"FlyCoral <{SENDER_EMAIL}>"
    msg["To"] = RECIPIENT_EMAIL

    html_content = generate_email_html()
    msg.attach(MIMEText(html_content, "html"))

    try:
        print(f"Conectando a {SMTP_SERVER}:{SMTP_PORT} vía SSL...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, YAHOO_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())
        print(f"✔ Alerta enviada con éxito a {RECIPIENT_EMAIL}")
        return True
    except Exception as e:
        print(f"✖ Error enviando el correo: {e}")
        return False

if __name__ == "__main__":
    send_flight_alert()
