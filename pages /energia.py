import time
import json
import streamlit as st

# ─────────────────────────────────────────────
# CARGA SEGURA DE PAHO-MQTT (Requiere paho-mqtt en requirements.txt)
# ─────────────────────────────────────────────
try:
    import paho.mqtt.client as paho
    MQTT_DISPONIBLE = True
except ModuleNotFoundError:
    paho = None
    MQTT_DISPONIBLE = False

def crear_cliente_mqtt(client_id):
    """Crea el cliente MQTT compatible con paho-mqtt 1.x y 2.x."""
    if hasattr(paho, "CallbackAPIVersion"):
        return paho.Client(paho.CallbackAPIVersion.VERSION1, client_id)
    return paho.Client(client_id)

# Configuración protegida por si se abre directo o desde el Panel Principal
try:
    st.set_page_config(
        page_title="Consumo de Energía - Nevera Inteligente",
        page_icon="⚡",
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
    border: 2.5px solid #4E8C6E;
    border-radius: 999px;
    padding: 8px 20px;
    text-align: center;
    color: #264E3B;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 600;
    letter-spacing: 1.2px;
    font-size: 1rem;
    text-transform: uppercase;
    box-shadow: 0 4px 0 rgba(38, 78, 59, 0.3), 0 6px 14px rgba(38, 56, 52, 0.14);
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
    margin-bottom: 16px;
}

.led-title {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(134, 197, 165, 0.14);
    border: 1.5px solid rgba(134, 197, 165, 0.55);
    color: #CFE9DB;
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

/* Tarjeta en la puerta con línea y tabla de energía */
.energy-guide-card {
    background: rgba(247, 244, 238, 0.94);
    border: 3px solid #F7F4EE;
    border-radius: 20px;
    padding: 16px;
    margin-bottom: 16px;
    box-shadow: 0 6px 14px rgba(33, 64, 58, 0.14);
}

.guide-title {
    font-family: 'Fredoka', cursive, sans-serif;
    color: #21403A;
    font-size: 0.98rem;
    font-weight: 600;
    margin-bottom: 10px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* Línea visual de zonas de energía de la nevera */
.energy-line-bar {
    display: flex;
    width: 100%;
    height: 28px;
    border-radius: 999px;
    overflow: hidden;
    border: 2px solid #FFFFFF;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
    margin-bottom: 6px;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    color: #FFFFFF;
}

.seg-danger {
    width: 18%;
    background: #C85A48;
    display: flex;
    align-items: center;
    justify-content: center;
}

.seg-eco {
    width: 24%;
    background: #4E8C6E;
    display: flex;
    align-items: center;
    justify-content: center;
}

.seg-normal {
    width: 33%;
    background: #4384A6;
    display: flex;
    align-items: center;
    justify-content: center;
}

.seg-turbo {
    width: 25%;
    background: #3B5B8C;
    display: flex;
    align-items: center;
    justify-content: center;
}

.energy-scale-labels {
    display: flex;
    justify-content: space-between;
    font-size: 0.72rem;
    font-weight: 800;
    color: #475569;
    margin-bottom: 12px;
    padding: 0 4px;
}

/* Tabla de conservación de alimentos por nivel de energía */
.energy-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.81rem;
    color: #1E293B;
}

.energy-table th {
    background-color: #E2ECE8;
    color: #21403A;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 600;
    text-align: left;
    padding: 8px 10px;
    border-bottom: 2px solid #B9D2CA;
}

.energy-table td {
    padding: 8px 10px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
}

.energy-table tr:last-child td {
    border-bottom: none;
}

.badge-mode {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 999px;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 600;
    font-size: 0.74rem;
    color: #FFFFFF;
    white-space: nowrap;
}

.b-zero { background-color: #C85A48; }
.b-eco { background-color: #4E8C6E; }
.b-norm { background-color: #4384A6; }
.b-turbo { background-color: #3B5B8C; }

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

/* Nota adhesiva color crema en la puerta de la nevera */
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

.section-label {
    color: #21403A;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.98rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin: 10px 0 10px 0;
    text-align: center;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.45);
}

/* Botones táctiles 3D en la puerta de la nevera */
div.stButton > button,
[data-testid="stButton"] > button {
    width: 100%;
    min-height: 62px;
    background: linear-gradient(135deg, #4E8C6E 0%, #386F54 100%) !important;
    color: #FBF9F5 !important;
    border: 3px solid #F7F4EE !important;
    border-radius: 18px !important;
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    box-shadow: 0 6px 0 #234A37, 0 10px 16px rgba(0, 0, 0, 0.15) !important;
    margin-bottom: 8px;
}

div.stButton > button p,
[data-testid="stButton"] > button p,
div.stButton > button span {
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1rem !important;
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
    box-shadow: 0 3px 0 #234A37 !important;
}

/* Texto del slider sobre la nevera */
.stSlider label p {
    color: #1B3631 !important;
    font-family: 'Nunito', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.94rem !important;
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

# Estado inicial del slider
if "nivel_energia" not in st.session_state:
    st.session_state.nivel_energia = 50.0

# ─────────────────────────────────────────────
# CONFIGURACIÓN MQTT PARA CONECTAR LA NEVERA CON WOKWI
# ─────────────────────────────────────────────
broker = "157.230.214.127"
port = 1883

def on_publish(client, userdata, result):
    print("Dato de energía de la nevera publicado con éxito \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(1)
    message_received = str(message.payload.decode("utf-8"))
    st.info(f"🛰️ Respuesta de la nevera en Wokwi: {message_received}")

# ─────────────────────────────────────────────
# 1. PLACA SUPERIOR DE LA NEVERA CON ÍCONO SVG E IMANES
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-top-bar">
    <div class="magnet-pill mag-left">🥑</div>
    <div class="brand-plate">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <rect x="5" y="2" width="14" height="20" rx="3" fill="#779F95" stroke="#36524B" stroke-width="1.8"/>
            <line x1="5" y1="9.5" x2="19" y2="9.5" stroke="#36524B" stroke-width="1.8"/>
            <line x1="8.5" y1="5" x2="8.5" y2="7.5" stroke="#F7F4EE" stroke-width="2" stroke-linecap="round"/>
            <line x1="8.5" y1="12" x2="8.5" y2="16" stroke="#F7F4EE" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>CONSUMO DE ENERGÍA</span>
    </div>
    <div class="magnet-pill mag-right">🍋</div>
</div>
""", unsafe_allow_html=True)

if not MQTT_DISPONIBLE:
    st.warning("⚠️ Falta instalar `paho-mqtt` en el servidor. Agrega `paho-mqtt` al archivo `requirements.txt` en la raíz de tu GitHub para activar el envío a Wokwi.")

# ─────────────────────────────────────────────
# 2. PANTALLA DIGITAL DE LA NEVERA (CONTROL REMOTO)
# ─────────────────────────────────────────────
st.markdown(f"""
<div class="led-screen">
    <div class="led-title">
        <span class="mqtt-dot"></span> CONTROL REMOTO DE NEVERA · BROKER {broker}
    </div>
    <h2 style="color: #F8FAFC !important; font-family: 'Fredoka', cursive, sans-serif; margin: 4px 0 6px 0; font-size: 1.4rem;">
        ⚡ Potencia del Compresor Fuera de Casa
    </h2>
    <p class="led-subtitle">
        Regula desde cualquier lugar cuánta energía recibe tu nevera: usa <b>Modo Eco (20%)</b> para ahorrar o <b>Modo Turbo (100%)</b> para enfriar tus alimentos al máximo.
    </p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 3. LÍNEA Y TABLA DE CONSERVACIÓN DE ALIMENTOS POR ENERGÍA
# ─────────────────────────────────────────────
st.markdown("""
<div class="energy-guide-card">
    <div class="guide-title">📊 Línea de Energía y Cuidado de Alimentos</div>
    <div class="energy-line-bar">
        <div class="seg-danger">0%-15% ⚠️</div>
        <div class="seg-eco">20% ECO 🌿</div>
        <div class="seg-normal">50%-75% DIARIO 🥛</div>
        <div class="seg-turbo">100% TURBO ❄️</div>
    </div>
    <div class="energy-scale-labels">
        <span>0% (Riesgo comida)</span>
        <span>20% (Modo Eco)</span>
        <span>60% (Ideal)</span>
        <span>100% (Modo Turbo)</span>
    </div>
    <table class="energy-table">
        <thead>
            <tr>
                <th>Nivel de Energía</th>
                <th>¿Cuándo usarlo en tu nevera?</th>
                <th>Impacto en tus Alimentos</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="badge-mode b-zero">0% · Sin frío</span></td>
                <td><b>Solo con la nevera vacía</b> (limpieza o descongelación).</td>
                <td>⚠️ <b>No recomendado con alimentos:</b> el calor interno daña carnes, lácteos y verduras.</td>
            </tr>
            <tr>
                <td><span class="badge-mode b-eco">20% · Modo Eco</span></td>
                <td>Fuera de casa, viajes o cuando hay pocos alimentos y la puerta no se abre.</td>
                <td>🌿 Conserva bebidas, frutas enteras y frascos con ahorro máximo de energía.</td>
            </tr>
            <tr>
                <td><span class="badge-mode b-norm">50%-75% · Normal</span></td>
                <td>Uso diario con mercado completo en el hogar.</td>
                <td>🥛 Mantiene la nevera a ~3.2°C y el congelador a -18°C para todo tipo de comida.</td>
            </tr>
            <tr>
                <td><span class="badge-mode b-turbo">100% · Modo Turbo</span></td>
                <td>Recién guardas el mercado, días muy calurosos o congelación rápida.</td>
                <td>❄️ Golpe de frío rápido para proteger carnes, pescados, helados y lácteos.</td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. DIVISOR DE PUERTAS Y NOTA ADHESIVA
# ─────────────────────────────────────────────
st.markdown("""
<div class="door-seal-wrap">
    <div class="door-seal"></div>
    <div class="fridge-handle"></div>
</div>
<div class="sticky-note">
    <div class="sticky-pin"></div><br>
    💡 Consejo para tu nevera: nunca la dejes en <b>0%</b> si hay comida adentro; elige <b>20% (Modo Eco)</b> cuando salgas de casa.
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 5. CONTROL DEL COMPRESOR DE LA NEVERA (ON / ECO / OFF A WOKWI)
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">🔌 Compresor General de la Nevera</div>', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button('🟢 ENCENDER NEVERA (ON)', use_container_width=True):
        st.session_state.nivel_energia = 100.0
        if not MQTT_DISPONIBLE:
            st.error("Agrega `paho-mqtt` a `requirements.txt` para enviar comandos a Wokwi.")
        else:
            try:
                act1 = "ON"
                client1 = crear_cliente_mqtt("NEVERA-ON")
                client1.on_publish = on_publish
                client1.connect(broker, port)
                message = json.dumps({"Act1": act1})
                client1.publish("cmqtt_s", message)
                st.success("❄️ ¡Compresor de la nevera encendido al 100% en Wokwi!")
            except Exception as e:
                st.error(f"No se pudo conectar con el broker MQTT: {e}")

with col2:
    if st.button('🌿 ECO', use_container_width=True):
        st.session_state.nivel_energia = 25.0
        if not MQTT_DISPONIBLE:
            st.error("Agrega `paho-mqtt` a `requirements.txt` para enviar comandos a Wokwi.")
        else:
            try:
                client1 = crear_cliente_mqtt("NEVERA-ECO")
                client1.on_publish = on_publish
                client1.connect(broker, port)
                client1.publish("cmqtt_s", json.dumps({"Act1": "ON"}))
                client1.publish("cmqtt_a", json.dumps({"Analog": 25.0}))
                st.success("🌿 ¡Modo Eco activado al 25% en Wokwi!")
            except Exception as e:
                st.error(f"No se pudo conectar con el broker MQTT: {e}")

with col3:
    if st.button('🟠 MODO ESPERA (OFF)', use_container_width=True):
        st.session_state.nivel_energia = 0.0
        if not MQTT_DISPONIBLE:
            st.error("Agrega `paho-mqtt` a `requirements.txt` para enviar comandos a Wokwi.")
        else:
            try:
                act1 = "OFF"
                client1 = crear_cliente_mqtt("NEVERA-OFF")
                client1.on_publish = on_publish
                client1.connect(broker, port)
                message = json.dumps({"Act1": act1})
                client1.publish("cmqtt_s", message)
                st.warning("🌙 ¡Compresor en pausa (0%)! Recuerda no dejar comida perecedera sin refrigeración.")
            except Exception as e:
                st.error(f"No se pudo conectar con el broker MQTT: {e}")

# ─────────────────────────────────────────────
# 6. REGULADOR DE PORCENTAJE DE ENERGÍA (SLIDER A WOKWI)
# ─────────────────────────────────────────────
st.markdown('<div class="section-label">🎚️ Porcentaje de Energía (Eco 20% ↔ Turbo 100%)</div>', unsafe_allow_html=True)

values = st.slider(
    'Selecciona el porcentaje de energía que recibirá tu nevera:',
    min_value=0.0,
    max_value=100.0,
    key="nivel_energia"
)

# Visor dinámico que evalúa si el porcentaje protege o pone en riesgo la comida
if values == 0:
    color_visor = "#9E3B2B"
    icono_modo = "⚠️"
    nombre_modo = "0% — PELIGRO: NEVERA SIN ENERGÍA"
    detalle_modo = "No recomendable con alimentos adentro: se romperá la cadena de frío."
elif values < 20:
    color_visor = "#B8553D"
    icono_modo = "⚠️"
    nombre_modo = f"{values:.0f}% — ENERGÍA INSUFICIENTE PARA COMIDA FRESCA"
    detalle_modo = "Sube al menos al 20% (Modo Eco) para conservar tus alimentos seguros."
elif values <= 35:
    color_visor = "#386F54"
    icono_modo = "🌿"
    nombre_modo = f"{values:.0f}% — MODO ECO (AHORRO FUERA DE CASA)"
    detalle_modo = "Consumo mínimo ideal cuando estás fuera de casa y la nevera permanece cerrada."
elif values <= 79:
    color_visor = "#2D6685"
    icono_modo = "🥛"
    nombre_modo = f"{values:.0f}% — MODO FRESCURA DIARIA"
    detalle_modo = "Potencia equilibrada para lácteos, frutas, verduras y congelados."
else:
    color_visor = "#2A4470"
    icono_modo = "❄️"
    nombre_modo = f"{values:.0f}% — MODO TURBO (ENFRIAMIENTO RÁPIDO)"
    detalle_modo = "Potencia máxima para enfriar mercado recién guardado o congelar rápido."

st.markdown(f"""
<div style="background-color: {color_visor}; border: 3px solid #F7F4EE; border-radius: 18px; padding: 14px 16px; text-align: center; margin-bottom: 14px; box-shadow: 0 5px 12px rgba(0,0,0,0.16);">
    <div style="font-family: 'Fredoka', cursive, sans-serif; font-size: 1.12rem; font-weight: 600; color: #FFFFFF;">
        {icono_modo} {nombre_modo}
    </div>
    <div style="font-family: 'Nunito', sans-serif; font-size: 0.85rem; color: #F1F5F9; margin-top: 4px;">
        {detalle_modo}
    </div>
</div>
""", unsafe_allow_html=True)

if st.button('📡 Enviar Energía a la Nevera (Wokwi)', use_container_width=True):
    if not MQTT_DISPONIBLE:
        st.error("Agrega `paho-mqtt` a `requirements.txt` para enviar comandos a Wokwi.")
    else:
        try:
            client1 = crear_cliente_mqtt("NEVERA-ENERGIA")
            client1.on_publish = on_publish
            client1.connect(broker, port)
            message = json.dumps({"Analog": float(values)})
            client1.publish("cmqtt_a", message)
            if values == 0:
                st.warning("⚠️ Se envió 0% de energía a la nevera en Wokwi. ¡Retira los alimentos para que no se dañen!")
            else:
                st.success(f"🚀 ¡Energía de la nevera ajustada al {values}% y enviada a Wokwi con éxito!")
        except Exception as e:
            st.error(f"No se pudo enviar el porcentaje al broker MQTT: {e}")

# ─────────────────────────────────────────────
# 7. IMANES DE COMIDA EN LA BASE DE LA PUERTA
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-magnets-footer">
    🧊 🧀 🥕 🍋 🫐 🥛
</div>
""", unsafe_allow_html=True)
