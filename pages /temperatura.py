import json
import time
import streamlit as st

# ─────────────────────────────────────────────
# CARGA SEGURA DE PAHO-MQTT (Compatible con v1.x y v2.x)
# ─────────────────────────────────────────────
try:
    import paho.mqtt.client as mqtt
    MQTT_DISPONIBLE = True
except ModuleNotFoundError:
    mqtt = None
    MQTT_DISPONIBLE = False

def crear_cliente_mqtt(client_id):
    """Crea el cliente MQTT compatible con paho-mqtt 1.x y 2.x."""
    if hasattr(mqtt, "CallbackAPIVersion"):
        return mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id=client_id)
    return mqtt.Client(client_id=client_id)

# Configuración protegida por si se abre directo o desde el Panel Principal
try:
    st.set_page_config(
        page_title="Control de Temperatura y Humedad - Nevera Inteligente",
        page_icon="🌡️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
except Exception:
    pass

# ─────────────────────────────────────────────
# ESTILOS CSS: PUERTA DE LA NEVERA RETRO (MISMA TEMÁTICA DEL PROYECTO)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@600;700;800&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}

/* Fondo de cocina cálida con azulejos suaves y mate */
.stApp {
    background-color: #EFECE6 !important;
    background-image:
        linear-gradient(90deg, rgba(168, 159, 145, 0.14) 1px, transparent 1px),
        linear-gradient(rgba(168, 159, 145, 0.14) 1px, transparent 1px),
        radial-gradient(circle at 15% 15%, rgba(143, 184, 174, 0.22), transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(217, 128, 102, 0.16), transparent 45%) !important;
    background-size: 38px 38px, 38px 38px, 100% 100%, 100% 100% !important;
    font-family: 'Nunito', sans-serif !important;
}

/* Cuerpo principal de la nevera retro verde salvia mate */
.main .block-container,
[data-testid="stMainBlockContainer"] {
    background: linear-gradient(165deg, #B9D2CA 0%, #92B6AC 48%, #779F95 100%);
    border-radius: 40px;
    border: 8px solid #F7F4EE;
    outline: 4px solid #5F867C;
    box-shadow:
        inset 10px 10px 24px rgba(255, 255, 255, 0.45),
        inset -10px -12px 24px rgba(34, 62, 56, 0.22),
        0 24px 48px rgba(38, 56, 52, 0.25);
    padding: 2rem 2.2rem 2.4rem 2.2rem !important;
    max-width: 600px !important;
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
}

/* Barra superior con imanes discretos y placa retro de la nevera */
.fridge-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.1rem;
    gap: 10px;
}

.magnet-pill {
    background: #F7F4EE;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.2rem;
    box-shadow: 0 3px 0 rgba(45, 74, 67, 0.22), 0 5px 10px rgba(0, 0, 0, 0.12);
    border: 2.5px solid #E6DEC8;
    user-select: none;
}

.mag-left { transform: rotate(-10deg); }
.mag-right { transform: rotate(10deg); }

.brand-plate {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: linear-gradient(180deg, #FBF9F5 0%, #EAE4D8 100%);
    border: 2.5px solid #4384A6;
    border-radius: 999px;
    padding: 8px 20px;
    text-align: center;
    color: #1E465C;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 600;
    letter-spacing: 1.2px;
    font-size: 1rem;
    text-transform: uppercase;
    box-shadow: 0 4px 0 rgba(30, 70, 92, 0.3), 0 6px 14px rgba(38, 56, 52, 0.14);
}

/* Pantalla digital de la nevera */
.led-screen {
    background: linear-gradient(145deg, #1E293B 0%, #263449 55%, #1A2433 100%);
    border: 4px solid #DDD3BE;
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    box-shadow:
        0 6px 0 rgba(45, 74, 67, 0.28),
        inset 0 0 18px rgba(148, 197, 219, 0.12);
    margin-bottom: 14px;
}

.led-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(147, 197, 224, 0.16);
    border: 1.5px solid rgba(147, 197, 224, 0.55);
    color: #D7EEFA;
    border-radius: 999px;
    padding: 4px 14px;
    font-family: 'Nunito', sans-serif;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.mqtt-dot {
    width: 8px;
    height: 8px;
    background-color: #74C69D;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 6px rgba(116, 198, 157, 0.8);
}

.led-subtitle {
    color: #CBD5E1 !important;
    font-size: 0.88rem;
    margin: 4px 0 0 0;
    line-height: 1.4;
}

.led-metrics {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 14px;
    flex-wrap: wrap;
    margin-top: 14px;
}

.metric-box {
    flex: 1;
    min-width: 170px;
    border-radius: 16px;
    padding: 14px 12px;
    text-align: center;
}

.metric-temp {
    background: linear-gradient(180deg, rgba(147, 197, 224, 0.2), rgba(71, 124, 160, 0.14));
    border: 1.5px solid rgba(147, 197, 224, 0.55);
}

.metric-hum {
    background: linear-gradient(180deg, rgba(125, 196, 178, 0.2), rgba(79, 138, 125, 0.14));
    border: 1.5px solid rgba(138, 206, 190, 0.55);
}

.metric-icon {
    font-size: 1.3rem;
    margin-bottom: 4px;
    letter-spacing: 3px;
}

.metric-value {
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 2.1rem;
    font-weight: 600;
    line-height: 1.1;
}

.metric-temp .metric-value { color: #CBE8F8; }
.metric-hum .metric-value { color: #B8EBD9; }

.metric-label {
    font-family: 'Nunito', sans-serif;
    font-size: 0.78rem;
    font-weight: 800;
    color: #E2E8F0;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 6px;
}

.metric-sub {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    color: #94A3B8;
    margin-top: 2px;
}

/* Sello divisor de puertas y manija cromada */
.door-seal-wrap {
    position: relative;
    margin: 20px -2.2rem 16px -2.2rem;
}

.door-seal {
    height: 12px;
    background: linear-gradient(180deg, #4E726A 0%, #36524B 55%, #5A8178 100%);
    border-top: 2px solid rgba(255, 255, 255, 0.55);
    border-bottom: 2px solid rgba(255, 255, 255, 0.3);
    box-shadow: 0 3px 6px rgba(27, 46, 42, 0.25);
}

.fridge-handle {
    width: 145px;
    height: 16px;
    background: linear-gradient(180deg, #F8F7F4 0%, #DCD8CE 55%, #BFC4C0 100%);
    border: 2px solid #8A9691;
    border-radius: 999px;
    margin: 10px auto 0 auto;
    box-shadow: 0 4px 8px rgba(30, 41, 59, 0.18), inset 0 2px 2px #FFFFFF;
}

/* Nota adhesiva color crema */
.sticky-note {
    background: linear-gradient(180deg, #F8F0D2 0%, #EFE2B5 100%);
    color: #544626;
    border-radius: 14px 14px 24px 14px;
    padding: 12px 16px;
    margin: 0 auto 16px auto;
    text-align: center;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.93rem;
    font-weight: 500;
    box-shadow: 0 5px 0 rgba(145, 118, 63, 0.22), 0 8px 16px rgba(0, 0, 0, 0.1);
    transform: rotate(-0.6deg);
    border: 2px solid #FBF6E6;
}

.sticky-pin {
    display: inline-block;
    width: 12px;
    height: 12px;
    background: radial-gradient(circle at 35% 35%, #E08A74, #B84A39);
    border-radius: 50%;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.28);
    margin-bottom: 3px;
}

/* Tarjetas de diagnóstico y sugerencias de la nevera */
.diag-card {
    border-radius: 18px;
    padding: 16px 18px;
    margin-bottom: 14px;
    border: 3px solid #F7F4EE;
    box-shadow: 0 6px 14px rgba(0, 0, 0, 0.14);
    color: #FFFFFF;
}

.diag-safe {
    background: linear-gradient(135deg, #386F54 0%, #2B5942 100%);
}

.diag-warning {
    background: linear-gradient(135deg, #B86B35 0%, #965222 100%);
}

.diag-high {
    background: linear-gradient(135deg, #A84438 0%, #873227 100%);
}

.diag-cold {
    background: linear-gradient(135deg, #3B6E8C 0%, #29526B 100%);
}

.diag-title {
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 1.08rem;
    font-weight: 600;
    margin-bottom: 6px;
}

.diag-body {
    font-family: 'Nunito', sans-serif;
    font-size: 0.88rem;
    line-height: 1.45;
    color: #F8FAFC !important;
}

/* Tarjetas informativas estilo estante de nevera */
.fridge-card {
    background: rgba(247, 244, 238, 0.94);
    border: 3px solid #F7F4EE;
    border-radius: 18px;
    padding: 15px 16px;
    margin-bottom: 14px;
    box-shadow: 0 5px 12px rgba(33, 64, 58, 0.12);
    color: #1E293B;
}

.fridge-card h4 {
    font-family: 'Fredoka', cursive, sans-serif !important;
    color: #21403A !important;
    margin: 0 0 6px 0 !important;
    font-size: 0.98rem !important;
}

.fridge-card p, .fridge-card li {
    color: #334155 !important;
    font-size: 0.83rem !important;
    line-height: 1.42 !important;
    margin-bottom: 4px !important;
}

/* Botón táctil 3D en azul glaciar (módulo de temperatura) */
div.stButton > button,
[data-testid="stButton"] > button {
    width: 100%;
    min-height: 64px;
    background: linear-gradient(135deg, #4384A6 0%, #2D6685 100%) !important;
    color: #FBF9F5 !important;
    border: 3px solid #F7F4EE !important;
    border-radius: 18px !important;
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    box-shadow: 0 6px 0 #1E465C, 0 10px 16px rgba(0, 0, 0, 0.15) !important;
    margin-bottom: 10px;
}

div.stButton > button p,
[data-testid="stButton"] > button p,
div.stButton > button span {
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    color: #FBF9F5 !important;
    margin: 0 !important;
}

div.stButton > button:hover,
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px);
    filter: brightness(1.06);
    border-color: #EFE2B5 !important;
}

div.stButton > button:active,
[data-testid="stButton"] > button:active {
    transform: translateY(3px);
    box-shadow: 0 3px 0 #1E465C !important;
}

/* Imanes decorativos inferiores */
.fridge-magnets-footer {
    margin-top: 14px;
    background: rgba(247, 244, 238, 0.42);
    border: 2px dashed rgba(247, 244, 238, 0.75);
    border-radius: 18px;
    padding: 8px 14px;
    text-align: center;
    font-size: 1.25rem;
    letter-spacing: 10px;
    user-select: none;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# VARIABLES DE ESTADO Y FUNCIÓN DE CONEXIÓN MQTT
# ─────────────────────────────────────────────
if "sensor_data" not in st.session_state:
    st.session_state.sensor_data = None

def get_mqtt_message(broker, port, topic, client_id):
    """Obtiene la lectura de temperatura y humedad enviada desde Wokwi por MQTT."""
    if not MQTT_DISPONIBLE:
        return {"error": "La librería paho-mqtt no está instalada. Agrégala en requirements.txt."}

    message_received = {"received": False, "payload": None}

    def on_message(client, userdata, message):
        try:
            payload = json.loads(message.payload.decode("utf-8", errors="replace"))
            message_received["payload"] = payload
            message_received["received"] = True
        except Exception:
            message_received["payload"] = message.payload.decode("utf-8", errors="replace")
            message_received["received"] = True

    try:
        unique_id = f"{client_id}_{int(time.time())}"
        client = crear_cliente_mqtt(unique_id)
        client.on_message = on_message
        client.connect(broker, port, 60)
        client.subscribe(topic)
        client.loop_start()

        timeout = time.time() + 5
        while not message_received["received"] and time.time() < timeout:
            time.sleep(0.1)

        client.loop_stop()
        client.disconnect()

        return message_received["payload"]

    except Exception as e:
        return {"error": str(e)}

# ─────────────────────────────────────────────
# 1. PLACA SUPERIOR DE LA NEVERA CON ÍCONO SVG E IMANES
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-top-bar">
    <div class="magnet-pill mag-left">🥬</div>
    <div class="brand-plate">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <rect x="5" y="2" width="14" height="20" rx="3" fill="#779F95" stroke="#36524B" stroke-width="1.8"/>
            <line x1="5" y1="9.5" x2="19" y2="9.5" stroke="#36524B" stroke-width="1.8"/>
            <line x1="8.5" y1="5" x2="8.5" y2="7.5" stroke="#F7F4EE" stroke-width="2" stroke-linecap="round"/>
            <line x1="8.5" y1="12" x2="8.5" y2="16" stroke="#F7F4EE" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>CONTROL DE TEMPERATURA</span>
    </div>
    <div class="magnet-pill mag-right">🍓</div>
</div>
""", unsafe_allow_html=True)

# Valores actuales para mostrar en la pantalla digital
temp_mostrar = "-- °C"
hum_mostrar = "-- %"
estado_pantalla = "ESPERANDO LECTURA DE WOKWI"

if isinstance(st.session_state.sensor_data, dict) and "error" not in st.session_state.sensor_data:
    d = st.session_state.sensor_data
    t_raw = d.get("temperature", d.get("temp", d.get("Temperatura", 3.2)))
    h_raw = d.get("humidity", d.get("hum", d.get("Humedad", 65.0)))
    try:
        temp_mostrar = f"{float(t_raw):.1f}°C"
        hum_mostrar = f"{float(h_raw):.0f}%"
        estado_pantalla = "LECTURA MQTT ACTUALIZADA"
    except Exception:
        pass

# ─────────────────────────────────────────────
# 2. PANTALLA DIGITAL DE LA NEVERA (TEMPERATURA Y HUMEDAD)
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="led-screen">
    <div class="led-title">
        <span class="mqtt-dot"></span> {estado_pantalla} · SENSOR INTERNO
    </div>
    <h2 style="color: #F8FAFC !important; font-family: 'Fredoka', cursive, sans-serif; margin: 2px 0 4px 0; font-size: 1.38rem;">
        🌡️ Clima Interno y Frescura de Alimentos
    </h2>
    <p class="led-subtitle">
        Monitorea en tiempo real la temperatura y la humedad de tu nevera desde Wokwi para conservar tus alimentos frescos y detectar fallas a tiempo.
    </p>
    <div class="led-metrics">
        <div class="metric-box metric-temp">
            <div class="metric-icon">❄️🥛🍎</div>
            <div class="metric-value">{temp_mostrar}</div>
            <div class="metric-label">Temperatura Nevera</div>
            <div class="metric-sub">Rango ideal: 1.5°C a 5.0°C</div>
        </div>
        <div class="metric-box metric-hum">
            <div class="metric-icon">💧🥬🥕</div>
            <div class="metric-value">{hum_mostrar}</div>
            <div class="metric-label">Humedad Relativa</div>
            <div class="metric-sub">Rango ideal: 50% a 80%</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Configuración MQTT desplegable en la puerta para poder ajustar broker o tópico si se requiere
with st.expander("⚙️ Configuración de Enlace MQTT (Wokwi)", expanded=False):
    col_cfg1, col_cfg2 = st.columns(2)
    with col_cfg1:
        broker = st.text_input("Broker MQTT", value="broker.mqttdashboard.com", help="Dirección del broker MQTT")
        topic = st.text_input("Tópico del Sensor", value="Sensor/THP2", help="Tópico donde publica el sensor en Wokwi")
    with col_cfg2:
        port = st.number_input("Puerto", value=1883, min_value=1, max_value=65535)
        client_id = st.text_input("ID de Cliente", value="nevera_client_01")

# ─────────────────────────────────────────────
# 3. BOTÓN ÚNICO PARA REFRESCAR DATOS DESDE WOKWI
# ─────────────────────────────────────────────
if st.button("🔄 Actualizar Temperatura y Humedad de la Nevera", use_container_width=True):
    with st.spinner("🛰️ Consultando sensor de temperatura y humedad en Wokwi..."):
        sensor_data = get_mqtt_message(broker, int(port), topic, client_id)
        st.session_state.sensor_data = sensor_data
        if isinstance(sensor_data, dict) and "error" not in sensor_data:
            st.rerun()

# ─────────────────────────────────────────────
# 4. SELLO DIVISOR DE PUERTAS Y NOTA ADHESIVA
# ─────────────────────────────────────────────
st.markdown("""
<div class="door-seal-wrap">
    <div class="door-seal"></div>
    <div class="fridge-handle"></div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. PROCESAMIENTO, DIAGNÓSTICO Y SUGERENCIAS DE LA NEVERA
# ─────────────────────────────────────────────
if st.session_state.sensor_data is not None:
    data = st.session_state.sensor_data

    if isinstance(data, dict) and "error" in data:
        st.error(f"❌ No se pudo conectar con el sensor de la nevera: {data['error']}")
    elif isinstance(data, dict):
        st.success("✅ ¡Lectura recibida desde el sensor de la nevera en Wokwi!")

        temp = data.get("temperature", data.get("temp", data.get("Temperatura", 3.2)))
        hum = data.get("humidity", data.get("hum", data.get("Humedad", 65.0)))

        try:
            temp_val = float(temp)
            hum_val = float(hum)
        except Exception:
            temp_val = 3.2
            hum_val = 65.0

        # --- DIAGNÓSTICO DE TEMPERATURA ---
        if temp_val > 7.0:
            temp_clase = "diag-high"
            temp_titulo = f"🚨 TEMPERATURA ALTA ({temp_val:.1f}°C) — Riesgo en la Cadena de Frío"
            temp_sugerencia = (
                "La nevera está demasiado tibia y los lácteos, carnes o comidas preparadas pueden dañarse rápido.<br>"
                "<b>¿Qué revisar en tu nevera?</b><br>"
                "• Verifica que la <b>puerta esté bien cerrada</b> y que ningún envase impida el cierre.<br>"
                "• Revisa los <b>empaques de caucho</b> de la puerta por si están sueltos o dejan entrar aire caliente.<br>"
                "• Evita meter <b>ollas o alimentos calientes</b> y no tapes las rejillas internas de ventilación.<br>"
                "• Ve al módulo de <b>Consumo de Energía</b> y activa el <b>Modo Turbo (100%)</b> por un par de horas."
            )
        elif temp_val > 5.0:
            temp_clase = "diag-warning"
            temp_titulo = f"⚠️ TEMPERATURA LIGERAMENTE ELEVADA ({temp_val:.1f}°C) — Precaución"
            temp_sugerencia = (
                "Está bien para frutas y verduras, pero un poco alta para leche, quesos frescos o embutidos.<br>"
                "<b>¿Qué revisar en tu nevera?</b><br>"
                "• Reduce las aperturas frecuentes o prolongadas de la puerta.<br>"
                "• Sube ligeramente la potencia del compresor (entre <b>60% y 75%</b>)."
            )
        elif temp_val < 1.5:
            temp_clase = "diag-cold"
            temp_titulo = f"🧊 TEMPERATURA MUY BAJA ({temp_val:.1f}°C) — Riesgo de Escarcha en Frescos"
            temp_sugerencia = (
                "La zona general está demasiado fría y puede congelar o quemar hojas verdes (lechuga, espinaca), frutas y huevos.<br>"
                "<b>¿Qué revisar en tu nevera?</b><br>"
                "• Revisa que el <b>termostato o conducto del congelador</b> no esté abierto al máximo.<br>"
                "• Aleja las verduras y líquidos de la pared del fondo.<br>"
                "• Baja un poco el porcentaje de energía hacia un rango medio (50%) o <b>Modo Eco (25%)</b>."
            )
        else:
            temp_clase = "diag-safe"
            temp_titulo = f"❄️ TEMPERATURA ÓPTIMA ({temp_val:.1f}°C) — Frescura Ideal"
            temp_sugerencia = (
                "Tu nevera está en el punto perfecto de refrigeración. Los lácteos, frutas, verduras y carnes frías se conservan seguros sin gastar energía de más."
            )

        # --- DIAGNÓSTICO DE HUMEDAD ---
        if hum_val > 80.0:
            hum_clase = "diag-high"
            hum_titulo = f"💧 HUMEDAD MUY ALTA ({hum_val:.0f}%) — Exceso de Condensación"
            hum_sugerencia = (
                "El exceso de humedad forma gotas en las paredes y acelera la aparición de moho en fresas, tomates, panes y quesos.<br>"
                "<b>¿Qué revisar en tu nevera?</b><br>"
                "• Revisa que el <b>orificio de drenaje</b> al fondo de la nevera no esté obstruido.<br>"
                "• Comprueba que los <b>empaques de la puerta</b> sellen bien (el aire húmedo exterior crea condensación).<br>"
                "• Tapa sopas, jarras y alimentos líquidos, y seca las paredes internas con un paño limpio."
            )
        elif hum_val < 50.0:
            hum_clase = "diag-warning"
            hum_titulo = f"🏜️ HUMEDAD BAJA ({hum_val:.0f}%) — Ambiente Frío y Seco"
            hum_sugerencia = (
                "El aire interno está muy seco y puede marchitar verduras, resecar quesos o endurecer carnes descubiertas.<br>"
                "<b>¿Qué revisar en tu nevera?</b><br>"
                "• Guarda siempre las frutas y verduras dentro de los <b>cajones inferiores (crispers)</b>.<br>"
                "• Usa <b>recipientes herméticos</b> o bolsas reutilizables para que los alimentos no pierdan su humedad natural."
            )
        else:
            hum_clase = "diag-safe"
            hum_titulo = f"🥬 HUMEDAD EQUILIBRADA ({hum_val:.0f}%) — Conservación Perfecta"
            hum_sugerencia = (
                "El nivel de humedad mantiene las verduras crujientes y evita tanto la resequedad como el exceso de gotas de condensación."
            )

        st.markdown(f"""
        <div class="diag-card {temp_clase}">
            <div class="diag-title">{temp_titulo}</div>
            <div class="diag-body">{temp_sugerencia}</div>
        </div>
        <div class="diag-card {hum_clase}">
            <div class="diag-title">{hum_titulo}</div>
            <div class="diag-body">{hum_sugerencia}</div>
        </div>
        """, unsafe_allow_html=True)

        # Tarjetas educativas de referencia rápida en la puerta
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("""
            <div class="fridge-card">
                <h4>🌡️ Guía Rápida de Temperatura</h4>
                <ul>
                    <li><b>1.5°C a 5.0°C:</b> Ideal para el refrigerador general.</li>
                    <li><b>&gt; 7.0°C:</b> Revisar cierre de puerta, empaques y ventilación.</li>
                    <li><b>&lt; 1.5°C:</b> Riesgo de escarcha en vegetales y bebidas.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        with col_g2:
            st.markdown("""
            <div class="fridge-card">
                <h4>💧 Guía Rápida de Humedad</h4>
                <ul>
                    <li><b>50% a 80%:</b> Verduras frescas sin condensación.</li>
                    <li><b>&gt; 80%:</b> Limpiar drenaje interno y tapar líquidos.</li>
                    <li><b>&lt; 50%:</b> Usar cajones inferiores y envases cerrados.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📂 Ver trama de datos recibida desde Wokwi (MQTT JSON)"):
            st.json(data)
    else:
        st.info(f"📡 Mensaje recibido desde Wokwi: `{data}` (Envía un JSON como `{{\"temp\": 3.5, \"hum\": 65}}` para ver el diagnóstico completo).")
else:
    st.markdown("""
    <div class="sticky-note">
        <div class="sticky-pin"></div><br>
        👆 Presiona el botón <b>"Actualizar Temperatura y Humedad de la Nevera"</b> para recibir los datos en vivo desde tu simulador en Wokwi y ver las recomendaciones de cuidado.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 6. IMANES DE COMIDA EN LA BASE DE LA PUERTA
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-magnets-footer">
    🧊 🧀 🥕 🍋 🫐 🥛
</div>
""", unsafe_allow_html=True)
