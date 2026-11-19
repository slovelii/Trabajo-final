import os
import base64
import requests
import streamlit as st

try:
    from openai import OpenAI
    OPENAI_DISPONIBLE = True
except ModuleNotFoundError:
    OpenAI = None
    OPENAI_DISPONIBLE = False

# Configuración protegida por si se abre directo o desde el Panel Principal
try:
    st.set_page_config(
        page_title="Gestión de Inventario - Nevera Inteligente",
        page_icon="🥗",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
except Exception:
    pass

def encode_image(image_data):
    """Codifica tanto archivos subidos/cámara como bytes descargados de una URL."""
    raw_bytes = image_data if isinstance(image_data, bytes) else image_data.getvalue()
    return base64.b64encode(raw_bytes).decode("utf-8")

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

/* Barra superior con imanes discretos y placa retro */
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
    border: 2.5px solid #C96A52;
    border-radius: 999px;
    padding: 8px 20px;
    text-align: center;
    color: #9E4733;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 600;
    letter-spacing: 1.2px;
    font-size: 1rem;
    text-transform: uppercase;
    box-shadow: 0 4px 0 rgba(158, 71, 51, 0.35), 0 6px 14px rgba(38, 56, 52, 0.14);
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
    background: rgba(212, 113, 87, 0.2);
    border: 1.5px solid rgba(224, 138, 116, 0.65);
    color: #FCDAD2;
    border-radius: 999px;
    padding: 4px 14px;
    font-family: 'Nunito', sans-serif;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.ai-dot {
    width: 8px;
    height: 8px;
    background-color: #F4A261;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 6px rgba(244, 162, 97, 0.85);
}

.led-subtitle {
    color: #CBD5E1 !important;
    font-size: 0.88rem;
    margin: 4px 0 0 0;
    line-height: 1.4;
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

/* Tarjeta tipo estante de la nevera para resultados de la IA */
.fridge-shelf {
    background: rgba(247, 244, 238, 0.95) !important;
    border: 3px solid #F7F4EE;
    border-left: 6px solid #C96A52;
    border-radius: 20px;
    padding: 18px 20px;
    margin-top: 14px;
    margin-bottom: 14px;
    box-shadow: 0 6px 14px rgba(33, 64, 58, 0.14);
    color: #1E293B !important;
}

.fridge-shelf h3 {
    font-family: 'Fredoka', cursive, sans-serif !important;
    color: #9E4733 !important;
    margin-top: 0 !important;
    font-size: 1.15rem !important;
}

.fridge-shelf p, .fridge-shelf li {
    color: #334155 !important;
    font-size: 0.9rem !important;
    line-height: 1.5 !important;
}

/* Botón táctil 3D en Terracota (color del módulo de Inventario) */
div.stButton > button,
[data-testid="stButton"] > button {
    width: 100%;
    min-height: 62px;
    background: linear-gradient(135deg, #D47157 0%, #B8553D 100%) !important;
    color: #FBF9F5 !important;
    border: 3px solid #F7F4EE !important;
    border-radius: 18px !important;
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    box-shadow: 0 6px 0 #843A28, 0 10px 16px rgba(0, 0, 0, 0.15) !important;
    margin-top: 8px;
    margin-bottom: 8px;
}

div.stButton > button p,
[data-testid="stButton"] > button p,
div.stButton > button span {
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.02rem !important;
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
    box-shadow: 0 3px 0 #843A28 !important;
}

/* Legibilidad de etiquetas sobre la puerta */
.stToggle label p, .stTextArea label p, .stTextInput label p, .stFileUploader label p, .stCameraInput label p {
    color: #1B3631 !important;
    font-weight: 800 !important;
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

if "foto_camara_externa" not in st.session_state:
    st.session_state.foto_camara_externa = None

# ─────────────────────────────────────────────
# 1. PLACA SUPERIOR DE LA NEVERA CON ÍCONO SVG E IMANES
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-top-bar">
    <div class="magnet-pill mag-left">🥗</div>
    <div class="brand-plate">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <rect x="5" y="2" width="14" height="20" rx="3" fill="#779F95" stroke="#36524B" stroke-width="1.8"/>
            <line x1="5" y1="9.5" x2="19" y2="9.5" stroke="#36524B" stroke-width="1.8"/>
            <line x1="8.5" y1="5" x2="8.5" y2="7.5" stroke="#F7F4EE" stroke-width="2" stroke-linecap="round"/>
            <line x1="8.5" y1="12" x2="8.5" y2="16" stroke="#F7F4EE" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <span>GESTIÓN DE INVENTARIO</span>
    </div>
    <div class="magnet-pill mag-right">🧀</div>
</div>
""", unsafe_allow_html=True)

if not OPENAI_DISPONIBLE:
    st.warning("⚠️ Falta instalar `openai`. Agrégalo a `requirements.txt` en la raíz de tu GitHub junto a `streamlit`, `paho-mqtt` y `requests`.")

# ─────────────────────────────────────────────
# 2. PANTALLA DIGITAL DE LA NEVERA (VISIÓN IA)
# ─────────────────────────────────────────────
st.markdown("""
<div class="led-screen">
    <div class="led-title">
        <span class="ai-dot"></span> VISIÓN INTELIGENTE · INVENTARIO DE ALIMENTOS
    </div>
    <h2 style="color: #F8FAFC !important; font-family: 'Fredoka', cursive, sans-serif; margin: 2px 0 6px 0; font-size: 1.38rem;">
        📸 Escáner de Comida en tu Nevera
    </h2>
    <p class="led-subtitle">
        Conecta una <b>cámara externa (ESP32-CAM / IP)</b>, usa la cámara de tu dispositivo o sube una foto para que la IA audite tus alimentos.
    </p>
</div>
""", unsafe_allow_html=True)

# Configuración de Clave OpenAI dentro de la puerta (o desde st.secrets si existe)
api_key = os.environ.get("OPENAI_API_KEY", "")
if not api_key and "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]

with st.expander("🔑 Configurar Clave OpenAI", expanded=(not bool(api_key))):
    ke = st.text_input("Ingresa tu Clave API de OpenAI", type="password")
    if ke:
        api_key = ke
        os.environ["OPENAI_API_KEY"] = ke

client = OpenAI(api_key=api_key) if (api_key and OPENAI_DISPONIBLE) else None

# ─────────────────────────────────────────────
# 3. TRES MODOS DE CAPTURA: CÁMARA EXTERNA, CÁMARA LOCAL O FOTO
# ─────────────────────────────────────────────
tab_url, tab_camara, tab_foto = st.tabs([
    "🌐 Cámara Externa (URL)",
    "📸 Cámara Local",
    "🖼️ Subir Foto"
])

with tab_url:
    url_camara = st.text_input(
        "URL de captura de la cámara externa (ESP32-CAM / IP o imagen pública):",
        placeholder="Ej: http://tu-camara-o-ngrok/capture"
    )
    if st.button("📷 Capturar desde Cámara Externa", use_container_width=True):
        if not url_camara.strip():
            st.warning("⚠️ Ingresa primero la URL de la cámara externa.")
        else:
            try:
                with st.spinner("📡 Descargando imagen desde la cámara externa..."):
                    resp = requests.get(url_camara.strip(), timeout=8)
                    resp.raise_for_status()
                    st.session_state.foto_camara_externa = resp.content
                    st.success("✅ ¡Captura obtenida desde la cámara externa!")
            except Exception as e:
                st.error(f"❌ No se pudo conectar con la cámara externa: {e}")

with tab_camara:
    camera_file = st.camera_input("Apunta la cámara al interior de tu nevera y toma una captura:")

with tab_foto:
    uploaded_file = st.file_uploader("📥 O selecciona una foto de tu nevera o estante", type=["jpg", "png", "jpeg"])

# Selección automática de la imagen disponible
imagen_para_analizar = None
if camera_file is not None:
    imagen_para_analizar = camera_file
elif uploaded_file is not None:
    imagen_para_analizar = uploaded_file
elif st.session_state.foto_camara_externa is not None:
    imagen_para_analizar = st.session_state.foto_camara_externa

if imagen_para_analizar is not None:
    with st.expander("🖼️ Vista previa de tu nevera", expanded=True):
        st.image(imagen_para_analizar, caption="Imagen lista para analizar", use_container_width=True)
else:
    st.markdown("""
    <div class="sticky-note">
        <div class="sticky-pin"></div><br>
        🍓 Pega la URL de tu <b>cámara externa</b>, usa la cámara local o sube una foto para que la IA revise tus estantes.
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 4. SELLO DIVISOR DE PUERTAS Y CONTEXTO ADICIONAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="door-seal-wrap">
    <div class="door-seal"></div>
    <div class="fridge-handle"></div>
</div>
""", unsafe_allow_html=True)

show_details = st.toggle("🔍 ¿Quieres hacer una pregunta específica sobre tus alimentos?", value=False)

additional_details = ""
if show_details:
    additional_details = st.text_area(
        "Ej: ¿Qué receta puedo hacer con esto? ¿Tengo suficientes lácteos o verduras?",
        disabled=not show_details
    )

analyze_button = st.button("✨ Auditar Inventario de la Nevera", use_container_width=True)

# ─────────────────────────────────────────────
# 5. ANÁLISIS CON IA (VISIÓN GPT-4O PARA NEVERA)
# ─────────────────────────────────────────────
if imagen_para_analizar is not None and api_key and analyze_button and client:
    with st.spinner("🔍 Revisando estantes, frescura de alimentos y stock disponible..."):
        base64_image = encode_image(imagen_para_analizar)

        prompt_text = (
            "Eres el asistente experto de una nevera inteligente. Analiza la imagen del interior de la nevera proporcionada y da tu diagnóstico en español estructurado en tres categorías claras:\n"
            "1. 🥬 INVENTARIO DETECTADO: Enumera los alimentos, bebidas, frutas, verduras y recipientes visibles.\n"
            "2. ⏳ PRIORIDAD DE CONSUMO Y FRESCURA: Indica qué alimentos parecen más maduros, abiertos o perecederos para consumirlos pronto, o si alguno luce en mal estado.\n"
            "3. 🛒 QUÉ COMPRAR / 🛑 QUÉ DEJAR DE COMPRAR: Sugiere qué básicos faltan y advierte si ya hay suficientes productos repetidos para evitar desperdicio.\n"
            "Sé práctico, claro y directo."
        )

        if show_details and additional_details:
            prompt_text += f"\n\nPregunta o contexto adicional del usuario:\n{additional_details}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    },
                ],
            }
        ]

        try:
            full_response = ""
            message_placeholder = st.empty()
            for completion in client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=1200,
                stream=True
            ):
                if completion.choices[0].delta.content is not None:
                    full_response += completion.choices[0].delta.content
                    message_placeholder.markdown(f"""
                    <div class="fridge-shelf">
                        <h3>📋 Diagnóstico de tu Nevera:</h3>
                        {full_response}▌
                    </div>
                    """, unsafe_allow_html=True)

            message_placeholder.markdown(f"""
            <div class="fridge-shelf">
                <h3>📋 Diagnóstico de tu Nevera:</h3>
                {full_response}
            </div>
            """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Ocurrió un error al analizar la nevera: {e}")

else:
    if imagen_para_analizar is None and analyze_button:
        st.warning("⚠️ Por favor captura una imagen con la cámara externa/local o sube una foto de tu nevera primero.")
    if not api_key and analyze_button:
        st.warning("🔑 Por favor ingresa tu Clave API de OpenAI en el desplegable superior para activar el análisis.")

# ─────────────────────────────────────────────
# 6. IMANES DE COMIDA EN LA BASE DE LA PUERTA
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-magnets-footer">
    🧊 🧀 🥕 🍋 🫐 🥛
</div>
""", unsafe_allow_html=True)
