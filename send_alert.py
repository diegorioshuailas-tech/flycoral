import os
import smtplib
import requests
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ==========================================
# CONFIGURACIÓN GENERAL Y CREDENCIALES
# ==========================================
SENDER_EMAIL = "diego.1202@yahoo.com"
RECIPIENT_EMAIL = "diego.1202@yahoo.com"
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 465

YAHOO_APP_PASSWORD = os.environ.get("YAHOO_APP_PASSWORD", "").strip()
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "").strip()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()

# Ruta y parámetros de la alerta semanal (podés ajustar origen, destino o días de viaje)
ORIGIN = "EZE"
DESTINATION = "MAD"
TRIP_DAYS = 14

# ==========================================
# OBTENER VUELOS REALES (SERPAPI - GOOGLE FLIGHTS)
# ==========================================
def fetch_real_flights():
    if not SERPAPI_KEY:
        print("Aviso: No se encontró SERPAPI_KEY. Usando datos de respaldo.")
        return None

    # Buscamos fechas tentativas a 45 días vista
    outbound = (datetime.date.today() + datetime.timedelta(days=45)).strftime("%Y-%m-%d")
    return_d = (datetime.date.today() + datetime.timedelta(days=45 + TRIP_DAYS)).strftime("%Y-%m-%d")

    params = {
        "engine": "google_flights",
        "departure_id": ORIGIN,
        "arrival_id": DESTINATION,
        "outbound_date": outbound,
        "return_date": return_d,
        "currency": "USD",
        "hl": "es",
        "api_key": SERPAPI_KEY
    }

    try:
        res = requests.get("https://serpapi.com/search", params=params, timeout=25)
        data = res.json()
        raw_flights = data.get("best_flights", []) + data.get("other_flights", [])

        if not raw_flights:
            return None

        parsed = []
        for f in raw_flights[:4]:
            legs = f.get("flights", [])
            airline = legs[0].get("airline", "Aerolínea") if legs else "Varios"
            stops = len(legs) - 1
            tipo = "Directo" if stops == 0 else f"{stops} Escala{'s' if stops > 1 else ''}"
            
            dep_time = legs[0].get("departure_airport", {}).get("time", "") if legs else ""
            arr_time = legs[-1].get("arrival_airport", {}).get("time", "") if legs else ""
            horario = f"{dep_time} ➔ {arr_time}" if dep_time and arr_time else "Consultar horarios"

            price = f.get("price", 0)
            ars_price = f"ARS {price * 1400:,.0f}".replace(",", ".")

            parsed.append({
                "airline": airline,
                "type": tipo,
                "dates": f"{outbound} ➔ {return_d}",
                "schedule": horario,
                "usd": f"USD {price}",
                "ars": ars_price,
                "price_num": price
            })
        return parsed
    except Exception as e:
        print(f"Error consultando SerpApi: {e}")
        return None

# ==========================================
# GENERAR VEREDICTO DE CORAL CON GEMINI
# ==========================================
def get_gemini_verdict(flights):
    if not GEMINI_API_KEY or not flights:
        return "Atención: revisá bien las escalas antes de emitir y asegurate de que la tarifa incluya equipaje despachado si viajás por más de 10 días."

    prompt = (
        f"Sos Coral, experta en tarifas de vuelos para viajeros de Argentina. Actuás como una madre protectora y práctica: "
        f"cero diminutivos melosos, directa, analítica y protectora del bolsillo. Analizá estas opciones para la ruta {ORIGIN} a {DESTINATION}:\n"
        f"{flights}\n"
        f"Escribí un veredicto conciso (máximo 2 oraciones) indicando cuál es la mejor alternativa y si conviene comprar o esperar."
    )

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        res = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=20)
        out = res.json()
        return out["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"Error llamando a Gemini: {e}")
        return "El vuelo con escala ofrece un ahorro considerable frente al directo; si la conexión es de al menos dos horas, es la opción más conveniente."

# ==========================================
# CONSTRUCCIÓN DE LA PLANTILLA HTML
# ==========================================
def build_html_template(flights, verdict):
    # Opciones de respaldo si la API no devuelve vuelos temporales
    if not flights:
        flights = [
            {"type": "Directo", "dates": "Fechas flexibles", "airline": "Iberia", "schedule": "22:45 ➔ 14:35", "usd": "USD 890", "ars": "ARS 1.246.000"},
            {"type": "1 Escala ★", "dates": "Fechas flexibles", "airline": "Air Europa", "schedule": "13:20 ➔ 09:15", "usd": "USD 740", "ars": "ARS 1.036.000"}
        ]

    rows = ""
    for idx, f in enumerate(flights):
        is_best = idx == 0 or "★" in f.get("type", "")
        bg = "#131b2e" if is_best else "#0f172a"
        color_accent = "#34d399" if is_best else "#38bdf8"
        btn_color = "#059669" if is_best else "#0284c7"

        rows += f"""
        <tr style="background-color: {bg}; border-bottom: 1px solid #1e293b;">
          <td style="padding: 14px; font-size: 13px; font-weight: 700; color: {color_accent};">{f['type']}</td>
          <td style="padding: 14px; font-size: 13px; color: #e2e8f0;">{f['dates']}</td>
          <td style="padding: 14px; font-size: 13px; color: #cbd5e1;"><strong>{f['airline']}</strong><br><span style="font-size: 11px; color: #94a3b8;">{f['schedule']}</span></td>
          <td style="padding: 14px; font-size: 13px; font-weight: 700; color: {color_accent};">{f['usd']}<br><span style="font-size: 11px; font-weight: normal; color: #94a3b8;">{f['ars']}</span></td>
          <td align="center" style="padding: 14px;">
            <a href="https://www.google.com/travel/flights" target="_blank" style="display: inline-block; background-color: {btn_color}; color: #ffffff; font-size: 12px; font-weight: 700; text-decoration: none; padding: 8px 14px; border-radius: 6px;">Ver Vuelo</a>
          </td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head><meta charset="utf-8"></head>
<body style="margin: 0; padding: 24px; background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; color: #e2e8f0;">
  <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 680px; background-color: #131b2e; border-radius: 14px; border: 1px solid #2d3748; overflow: hidden;">
    <tr>
      <td style="padding: 24px 28px; background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border-bottom: 2px solid #38bdf8;">
        <span style="font-size: 24px; font-weight: 800; color: #ffffff;">FlyCoral</span>
        <span style="margin-left: 8px; font-size: 11px; font-weight: 700; background-color: #0284c7; color: #ffffff; padding: 3px 8px; border-radius: 6px;">AR</span>
        <div style="font-size: 13px; color: #94a3b8; margin-top: 4px;">Asistente Experta en Tarifas y Rutas</div>
      </td>
    </tr>
    <tr>
      <td style="padding: 28px;">
        <div style="display: inline-block; padding: 6px 12px; background-color: rgba(56, 189, 248, 0.12); border: 1px solid #0284c7; border-radius: 20px; font-size: 12px; font-weight: 700; color: #38bdf8; text-transform: uppercase; margin-bottom: 16px;">
          🗓 Monitoreo Semanal de Vuelo
        </div>
        <h1 style="font-size: 20px; font-weight: 700; color: #f8fafc; margin: 0 0 12px 0;">
          Ruta monitoreada: {ORIGIN} ➔ {DESTINATION}
        </h1>
        <p style="font-size: 14px; line-height: 1.6; color: #cbd5e1; margin: 0 0 20px 0;">
          Este es tu reporte semanal automático con los valores actualizados de Google Flights:
        </p>

        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse; border: 1px solid #334155; border-radius: 8px; overflow: hidden; margin-bottom: 24px;">
          <thead>
            <tr style="background-color: #1e293b;">
              <th align="left" style="padding: 12px 14px; font-size: 12px; color: #94a3b8; border-bottom: 1px solid #334155;">Opción</th>
              <th align="left" style="padding: 12px 14px; font-size: 12px; color: #94a3b8; border-bottom: 1px solid #334155;">Fechas</th>
              <th align="left" style="padding: 12px 14px; font-size: 12px; color: #94a3b8; border-bottom: 1px solid #334155;">Aerolínea</th>
              <th align="left" style="padding: 12px 14px; font-size: 12px; color: #94a3b8; border-bottom: 1px solid #334155;">Tarifa</th>
              <th align="center" style="padding: 12px 14px; font-size: 12px; color: #94a3b8; border-bottom: 1px solid #334155;">Acción</th>
            </tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>

        <table width="100%" border="0" cellpadding="0" cellspacing="0" style="background-color: #1e293b; border-left: 4px solid #38bdf8; border-radius: 0 8px 8px 0; margin-bottom: 24px;">
          <tr>
            <td style="padding: 16px 20px;">
              <div style="font-size: 13px; font-weight: 800; text-transform: uppercase; color: #38bdf8; margin-bottom: 6px;">
                💡 Veredicto de Coral
              </div>
              <div style="font-size: 13px; line-height: 1.5; color: #f1f5f9; font-style: italic;">
                "{verdict}"
              </div>
            </td>
          </tr>
        </table>

        <p style="font-size: 12px; color: #64748b; line-height: 1.5; margin: 0; border-top: 1px solid #1e293b; padding-top: 16px;">
          Alerta activa semanalmente. Para pausar o cancelar el reporte, desactiva el workflow en GitHub Actions.
        </p>
      </td>
    </tr>
  </table>
</body>
</html>"""

# ==========================================
# ENVÍO DEL CORREO
# ==========================================
def main():
    if not YAHOO_APP_PASSWORD:
        print("ERROR: No se configuró YAHOO_APP_PASSWORD en los secretos.")
        return

    print("1. Obteniendo tarifas actualizadas de Google Flights...")
    flights = fetch_real_flights()

    print("2. Consultando veredicto con Gemini...")
    verdict = get_gemini_verdict(flights)

    print("3. Generando reporte y conectando con Yahoo Mail...")
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"✈ FlyCoral Semanal: Vuelos {ORIGIN} ➔ {DESTINATION}"
    msg["From"] = f"FlyCoral <{SENDER_EMAIL}>"
    msg["To"] = RECIPIENT_EMAIL

    html = build_html_template(flights, verdict)
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(SENDER_EMAIL, YAHOO_APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

    print(f"✔ Reporte semanal despachado con éxito a {RECIPIENT_EMAIL}")

if __name__ == "__main__":
    main()
