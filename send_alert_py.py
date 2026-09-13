import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ==============================================================================
# CONFIGURACIÓN DE CORREO (YAHOO MAIL)
# ==============================================================================
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 465  # Puerto SSL

SENDER_EMAIL = os.environ.get("SENDER_EMAIL", "diego.1202@yahoo.com")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "diego.1202@yahoo.com")
YAHOO_APP_PASSWORD = os.environ.get("YAHOO_APP_PASSWORD", "pega_aqui_tu_clave_de_16_letras")

def build_alert_html(route, departure_date, return_date, flights, verdict, is_impossible_price=False):
    """
    Genera el HTML del correo electrónico con el diseño y tabla con líneas
    divisorias de FlyCoral.
    """
    badge_text = "🔥 ¡PRECIO IMPOSIBLE DETECTADO!" if is_impossible_price else "✈️ ALERTA PROGRAMADA DE VUELO"
    badge_bg = "#ffe4e6" if is_impossible_price else "#fce7f3"
    badge_color = "#e11d48" if is_impossible_price else "#be185d"

    rows_html = ""
    for f in flights:
        rows_html += f"""
        <tr style="border-bottom: 1px solid #cbd5e1;">
            <td style="padding: 10px; font-weight: bold; border: 1px solid #cbd5e1;">{f.get('type', 'Opción')}</td>
            <td style="padding: 10px; border: 1px solid #cbd5e1;">{f.get('dates', f'{departure_date} ➔ {return_date}')}</td>
            <td style="padding: 10px; border: 1px solid #cbd5e1;">{f.get('airline', 'Aerolínea')}</td>
            <td style="padding: 10px; border: 1px solid #cbd5e1;">{f.get('schedules', '--:--')}</td>
            <td style="padding: 10px; font-weight: bold; color: #0f172a; border: 1px solid #cbd5e1;">{f.get('price', '--')}</td>
            <td style="padding: 10px; text-align: center; border: 1px solid #cbd5e1;">
                <a href="{f.get('link', 'https://www.google.com/travel/flights')}" 
                   style="display: inline-block; padding: 7px 14px; background-color: #ffbee9; color: #0f172a; text-decoration: none; font-weight: bold; border-radius: 6px; font-size: 11px;">
                   👉 Ver y Reservar este Vuelo
                </a>
            </td>
        </tr>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 20px; color: #1e293b;">
        <div style="max-width: 680px; margin: 0 auto; background: #ffffff; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            
            <!-- Encabezado FlyCoral -->
            <div style="background-color: #0f172a; padding: 20px; text-align: left; border-bottom: 3px solid #ffbee9;">
                <h1 style="margin: 0; color: #ffffff; font-size: 20px; font-weight: bold;">
                    FlyCoral <span style="font-size: 11px; background: #ffbee9; color: #0f172a; padding: 2px 7px; border-radius: 4px; margin-left: 6px;">AR</span>
                </h1>
                <p style="margin: 4px 0 0 0; color: #94a3b8; font-size: 12px;">Asistente Experta de Vuelos</p>
            </div>

            <div style="padding: 24px;">
                <!-- Badge de Alerta -->
                <div style="display: inline-block; padding: 4px 10px; border-radius: 6px; background-color: {badge_bg}; color: {badge_color}; font-weight: bold; font-size: 11px; text-transform: uppercase; margin-bottom: 14px;">
                    {badge_text}
                </div>

                <h2 style="margin: 0 0 12px 0; font-size: 18px; color: #0f172a;">
                    Reporte de ruta: {route}
                </h2>

                <p style="font-size: 13px; color: #475569; line-height: 1.5; margin-bottom: 16px;">
                    Hola, ¿cómo estás? Acá estuve mirando las alternativas para esta ruta y consolidé las tarifas más sensatas para cuidar tu presupuesto:
                </p>

                <!-- Tabla de vuelos con bordes nítidos -->
                <div style="overflow-x: auto; margin-bottom: 20px;">
                    <table style="width: 100%; border-collapse: collapse; font-size: 12px; text-align: left; border: 1px solid #cbd5e1;">
                        <thead>
                            <tr style="background-color: #ffbee9; color: #0f172a;">
                                <th style="padding: 10px; border: 1px solid #cbd5e1;">Opción</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1;">Fecha</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1;">Aerolínea & Escala</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1;">Horarios</th>
                                <th style="padding: 10px; border: 1px solid #cbd5e1;">Tarifa USD / ARS</th>
                                <th style="padding: 10px; text-align: center; border: 1px solid #cbd5e1;">Link Directo</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>

                <!-- Veredicto de Coral -->
                <div style="border-left: 4px solid #ffbee9; background-color: #fdf2f8; padding: 12px 16px; border-radius: 0 8px 8px 0; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 12px; font-weight: bold; color: #831843;">Veredicto de Coral:</p>
                    <p style="margin: 4px 0 0 0; font-size: 13px; color: #475569; font-style: italic;">
                        "{verdict}"
                    </p>
                </div>

                <p style="font-size: 11px; color: #94a3b8; margin: 0; border-top: 1px solid #f1f5f9; padding-top: 12px;">
                    Este reporte fue generado y enviado automáticamente desde tu asistente FlyCoral con tu cuenta <strong>{SENDER_EMAIL}</strong>.
                </p>
            </div>
        </div>
    </body>
    </html>
    """

def send_flight_alert(recipient_email, subject, route, departure_date, return_date, flights, verdict, is_impossible=False):
    """
    Despacha el correo vía SSL por el servidor SMTP oficial de Yahoo Mail.
    """
    if not YAHOO_APP_PASSWORD or YAHOO_APP_PASSWORD == "pega_aqui_tu_clave_de_16_letras":
        print("⚠️ ERROR: Falta configurar YAHOO_APP_PASSWORD.")
        print("Generala en: https://login.yahoo.com/account/security -> Contraseñas de aplicaciones.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"FlyCoral <{SENDER_EMAIL}>"
    msg["To"] = recipient_email

    plain_text = f"Reporte FlyCoral para {route}.\nTarifa: {flights[0].get('price')} con {flights[0].get('airline')}.\nLink: {flights[0].get('link')}"
    html_body = build_alert_html(route, departure_date, return_date, flights, verdict, is_impossible)

    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    try:
        print(f"Conectando a {SMTP_SERVER}:{SMTP_PORT} vía SSL...")
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, YAHOO_APP_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"✅ ¡Correo enviado exitosamente a {recipient_email} desde {SENDER_EMAIL}!")
        return True
    except smtplib.SMTPAuthenticationError:
        print("❌ Error de autenticación: Yahoo rechazó la contraseña. Verificá que estés usando la 'Contraseña de aplicación' de 16 letras.")
        return False
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")
        return False

if __name__ == "__main__":
    # Ejemplo de vuelo para test o despacho programado
    sample_flights = [
        {
            "type": "Directo",
            "dates": "15 Oct ➔ 23 Oct",
            "airline": "Iberia / Level",
            "schedules": "22:45 (EZE) ➔ 14:35 (MAD)",
            "price": "USD 880 / ARS 1.260.000",
            "link": "https://www.google.com/travel/flights?q=Flights%20to%20MAD%20from%20EZE%20on%202026-10-15%20through%202026-10-23&curr=USD"
        },
        {
            "type": "1 Escala",
            "dates": "15 Oct ➔ 23 Oct",
            "airline": "Air Europa",
            "schedules": "13:20 (EZE) ➔ 09:15 (MAD)",
            "price": "USD 740 / ARS 1.060.000",
            "link": "https://www.google.com/travel/flights?q=Flights%20to%20MAD%20from%20EZE%20on%202026-10-15%20through%202026-10-23&curr=USD"
        }
    ]

    sample_verdict = "USD 740 para cruzar el charco es una tarifa excelente; con esa escala corta te ahorrás unos cuantos dólares para gastar en destino."

    print("--- Ejecutando envío de alerta FlyCoral vía Yahoo Mail ---")
    send_flight_alert(
        recipient_email=RECIPIENT_EMAIL,
        subject="✈️ Alerta FlyCoral: Buenos Aires a Madrid en precio conveniente",
        route="Buenos Aires (EZE) ➔ Madrid (MAD)",
        departure_date="2026-10-15",
        return_date="2026-10-23",
        flights=sample_flights,
        verdict=sample_verdict,
        is_impossible=False
    )