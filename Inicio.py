import streamlit as st
from pathlib import Path
import unicodedata

# Configuración inicial de la página
st.set_page_config(
    page_title="Panel de Control - Nevera Inteligente",
    layout="centered",
    initial_sidebar_state="collapsed"
)

if "pagina_activa" not in st.session_state:
    st.session_state.pagina_activa = "inicio"

def ir_a(nombre_pagina):
    st.session_state.pagina_activa = nombre_pagina

def normalizar(texto):
    """Elimina tildes, espacios invisibles y pasa a minúsculas."""
    texto_sin_tildes = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return texto_sin_tildes.strip().lower()

def encontrar_archivo_real(nombre_buscado):
    """Busca el archivo .py en todo el repositorio sin importar espacios en carpetas."""
    raiz = Path(__file__).resolve().parent
    objetivo = normalizar(nombre_buscado)
    for ruta in raiz.rglob("*.py"):
        if ruta.name != Path(__file__).name:
            if objetivo in normalizar(ruta.stem):
                return ruta
    return None

# Si el usuario entró a alguno de los 3 módulos:
if st.session_state.pagina_activa != "inicio":
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    if st.button("← Volver al Panel Principal"):
        st.session_state.pagina_activa = "inicio"
        st.rerun()

    ruta_archivo = encontrar_archivo_real(st.session_state.pagina_activa)

    if ruta_archivo and ruta_archivo.exists():
        codigo = ruta_archivo.read_text(encoding="utf-8")
        
        # Filtramos st.set_page_config y el botón viejo de switch_page para que no den error
        lineas_limpias = []
        for linea in codigo.splitlines():
            if "st.switch_page" in linea or "Volver al Panel Principal" in linea:
                continue
            lineas_limpias.append(linea)
        
        codigo_final = "\n".join(lineas_limpias).strip()
        
        # Si el archivo en GitHub solo tenía el botón de volver y nada más, mostramos aviso
        if codigo_final == "" or codigo_final == "import streamlit as st":
            st.info(f"Conectado exitosamente a `{ruta_archivo.name}`. Agrega aquí tus gráficas y controles de {st.session_state.pagina_activa}.")
        else:
            exec(codigo_final, globals())
    else:
        # Diagnóstico en pantalla: muestra todos los archivos que realmente existen en el servidor
        raiz = Path(__file__).resolve().parent
        archivos_en_servidor = [str(p.relative_to(raiz)) for p in raiz.rglob("*")]
        st.error(f"No se encontró '{st.session_state.pagina_activa}.py'.")
        st.write("Archivos detectados actualmente en tu servidor de Streamlit:", archivos_en_servidor)

    st.stop()

# =====================================================================
# INTERFAZ DE INICIO: NEVERA RETRO COLORIDA, SOBRIA E INTERACTIVA
# =====================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@600;700;800&display=swap');

/* Ocultar elementos nativos de Streamlit (menú, footer, header y barra lateral) */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}

/* Fondo de cocina cálida con azulejos suaves y mate */
.stApp {
    background-color: #EFECE6;
    background-image:
        linear-gradient(90deg, rgba(168, 159, 145, 0.14) 1px, transparent 1px),
        linear-gradient(rgba(168, 159, 145, 0.14) 1px, transparent 1px),
        radial-gradient(circle at 15% 15%, rgba(143, 184, 174, 0.22), transparent 45%),
        radial-gradient(circle at 85% 85%, rgba(217, 128, 102, 0.16), transparent 45%);
    background-size: 38px 38px, 38px 38px, 100% 100%, 100% 100%;
    font-family: 'Nunito', sans-serif;
}

/* Cuerpo principal estilo nevera retro verde salvia mate */
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
    max-width: 580px !important;
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
}

/* Barra superior con imanes discretos y placa retro */
.fridge-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.2rem;
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
    padding: 8px 22px;
    text-align: center;
    color: #9E4733;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 600;
    letter-spacing: 1.4px;
    font-size: 1.05rem;
    text-transform: uppercase;
    box-shadow: 0 4px 0 rgba(158, 71, 51, 0.35), 0 6px 14px rgba(38, 56, 52, 0.14);
}

/* Pantalla digital sobria empotrada en la puerta superior */
.led-screen {
    background: linear-gradient(145deg, #1E293B 0%, #263449 55%, #1A2433 100%);
    border: 4px solid #DDD3BE;
    border-radius: 22px;
    padding: 18px 18px 20px 18px;
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
    background: rgba(134, 197, 165, 0.14);
    border: 1.5px solid rgba(134, 197, 165, 0.55);
    color: #CFE9DB;
    border-radius: 999px;
    padding: 4px 14px;
    font-family: 'Nunito', sans-serif;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 1.1px;
    text-transform: uppercase;
    margin-bottom: 16px;
}

.mqtt-dot {
    width: 8px;
    height: 8px;
    background-color: #74C69D;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 6px rgba(116, 198, 157, 0.8);
}

.led-metrics {
    display: flex;
    justify-content: center;
    align-items: stretch;
    gap: 14px;
    flex-wrap: wrap;
}

.metric-box {
    flex: 1;
    min-width: 175px;
    border-radius: 16px;
    padding: 14px 12px;
    text-align: center;
}

.metric-fridge {
    background: linear-gradient(180deg, rgba(125, 196, 178, 0.18), rgba(79, 138, 125, 0.12));
    border: 1.5px solid rgba(138, 206, 190, 0.55);
}

.metric-freezer {
    background: linear-gradient(180deg, rgba(147, 197, 224, 0.18), rgba(71, 124, 160, 0.14));
    border: 1.5px solid rgba(147, 197, 224, 0.55);
}

.metric-icon {
    font-size: 1.3rem;
    margin-bottom: 4px;
    letter-spacing: 4px;
}

.metric-value {
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 2.15rem;
    font-weight: 600;
    line-height: 1.1;
}

.metric-fridge .metric-value { color: #B8EBD9; }
.metric-freezer .metric-value { color: #CBE8F8; }

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
    font-size: 0.7rem;
    color: #94A3B8;
    margin-top: 2px;
}

/* Sello divisor de puertas y manija cromada satinada */
.door-seal-wrap {
    position: relative;
    margin: 24px -2.2rem 20px -2.2rem;
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

/* Nota adhesiva color crema pegada a la puerta */
.sticky-note {
    background: linear-gradient(180deg, #F8F0D2 0%, #EFE2B5 100%);
    color: #544626;
    border-radius: 14px 14px 24px 14px;
    padding: 12px 18px;
    margin: 0 auto 18px auto;
    max-width: 94%;
    text-align: center;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.96rem;
    font-weight: 500;
    box-shadow: 0 5px 0 rgba(145, 118, 63, 0.22), 0 8px 16px rgba(0, 0, 0, 0.1);
    transform: rotate(-0.8deg);
    border: 2px solid #FBF6E6;
}

.sticky-pin {
    display: inline-block;
    width: 13px;
    height: 13px;
    background: radial-gradient(circle at 35% 35%, #E08A74, #B84A39);
    border-radius: 50%;
    box-shadow: 0 2px 3px rgba(0, 0, 0, 0.28);
    margin-bottom: 4px;
}

.section-label {
    color: #21403A;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.98rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 14px;
    text-align: center;
    text-shadow: 0 1px 0 rgba(255, 255, 255, 0.45);
}

/* Ocultar los marcadores invisibles para colorear cada botón */
[data-testid="stVerticalBlock"] > div:has(.btn-marker),
[data-testid="stElementContainer"]:has(.btn-marker),
.element-container:has(.btn-marker) {
    display: none !important;
}

/* Botones táctiles 3D con paleta colorida pero sobria */
div.stButton > button,
[data-testid="stButton"] > button {
    width: 100%;
    height: 74px;
    background: linear-gradient(180deg, #C96A52 0%, #B45740 100%);
    color: #FBF9F5 !important;
    border: 3px solid #F7F4EE !important;
    border-radius: 20px !important;
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.12rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    box-shadow: 0 7px 0 rgba(30, 41, 59, 0.25), 0 10px 18px rgba(0, 0, 0, 0.14);
    margin-bottom: 10px;
}

div.stButton > button p,
[data-testid="stButton"] > button p {
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.12rem !important;
    font-weight: 600 !important;
    color: #FBF9F5 !important;
    text-shadow: 0 1px 3px rgba(0, 0, 0, 0.22);
    margin: 0 !important;
}

div.stButton > button:hover,
[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) scale(1.01);
    filter: brightness(1.06);
    border-color: #EFE2B5 !important;
    box-shadow: 0 9px 0 rgba(30, 41, 59, 0.25), 0 14px 22px rgba(0, 0, 0, 0.18);
}

div.stButton > button:active,
[data-testid="stButton"] > button:active {
    transform: translateY(4px) scale(0.99);
    box-shadow: 0 3px 0 rgba(30, 41, 59, 0.25), 0 5px 10px rgba(0, 0, 0, 0.14);
}

/* Botón 1: Control de Temperatura (Azul Glaciar) */
[data-testid="stVerticalBlock"] > div:has(.marker-temp) + div button,
[data-testid="stElementContainer"]:has(.marker-temp) + [data-testid="stElementContainer"] button,
.element-container:has(.marker-temp) + .element-container button {
    background: linear-gradient(135deg, #4384A6 0%, #2D6685 100%) !important;
    box-shadow: 0 7px 0 #1E465C, 0 10px 18px rgba(30, 70, 92, 0.26) !important;
}

/* Botón 2: Gestión de Inventario (Terracota / Comida Fresca) */
[data-testid="stVerticalBlock"] > div:has(.marker-inv) + div button,
[data-testid="stElementContainer"]:has(.marker-inv) + [data-testid="stElementContainer"] button,
.element-container:has(.marker-inv) + .element-container button {
    background: linear-gradient(135deg, #D47157 0%, #B8553D 100%) !important;
    box-shadow: 0 7px 0 #843A28, 0 10px 18px rgba(132, 58, 40, 0.26) !important;
}

/* Botón 3: Consumo de Energía (Verde Hierba / Eco) */
[data-testid="stVerticalBlock"] > div:has(.marker-eco) + div button,
[data-testid="stElementContainer"]:has(.marker-eco) + [data-testid="stElementContainer"] button,
.element-container:has(.marker-eco) + .element-container button {
    background: linear-gradient(135deg, #4E8C6E 0%, #386F54 100%) !important;
    box-shadow: 0 7px 0 #234A37, 0 10px 18px rgba(35, 74, 55, 0.26) !important;
}

/* Franja decorativa inferior con imanes de alimentos */
.fridge-magnets-footer {
    margin-top: 14px;
    background: rgba(247, 244, 238, 0.42);
    border: 2px dashed rgba(247, 244, 238, 0.75);
    border-radius: 18px;
    padding: 9px 14px;
    text-align: center;
    font-size: 1.3rem;
    letter-spacing: 10px;
    user-select: none;
}
</style>
""", unsafe_allow_html=True)

# 1. Placa de marca superior con imanes discretos e ícono SVG de nevera
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
        <span>MI NEVERA INTERACTIVA</span>
    </div>
    <div class="magnet-pill mag-right">🍓</div>
</div>
""", unsafe_allow_html=True)

# 2. Pantalla digital con solo las 2 temperaturas iniciales (Nevera General y Congelador vía MQTT)
st.markdown("""
<div class="led-screen">
    <div class="led-title">
        <span class="mqtt-dot"></span> LECTURA MQTT · SISTEMA OPERATIVO
    </div>
    <div class="led-metrics">
        <div class="metric-box metric-fridge">
            <div class="metric-icon">🥬🥛🍎</div>
            <div class="metric-value">3.2°C</div>
            <div class="metric-label">Nevera General</div>
            <div class="metric-sub">Sensor principal MQTT</div>
        </div>
        <div class="metric-box metric-freezer">
            <div class="metric-icon">❄️🧊🍦</div>
            <div class="metric-value">-18.0°C</div>
            <div class="metric-label">Congelador</div>
            <div class="metric-sub">Sensor congelación MQTT</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Sello divisor de puertas y manija retro
st.markdown("""
<div class="door-seal-wrap">
    <div class="door-seal"></div>
    <div class="fridge-handle"></div>
</div>
""", unsafe_allow_html=True)

# 4. Nota adhesiva y panel de navegación (Puerta Inferior)
st.markdown("""
<div class="sticky-note">
    <div class="sticky-pin"></div><br>
    Explora y ajusta tu nevera a tu manera: elige un módulo para empezar ✨
</div>
<div class="section-label">Módulos de Monitoreo</div>
""", unsafe_allow_html=True)

# Botones de navegación sin usar st.switch_page (funcionalidad intacta)
st.markdown('<div class="btn-marker marker-temp"></div>', unsafe_allow_html=True)
if st.button("🌡️ CONTROL DE TEMPERATURA", use_container_width=True):
    ir_a("temperatura")
    st.rerun()

st.markdown('<div class="btn-marker marker-inv"></div>', unsafe_allow_html=True)
if st.button("🥗 GESTIÓN DE INVENTARIO", use_container_width=True):
    ir_a("inventario")
    st.rerun()

st.markdown('<div class="btn-marker marker-eco"></div>', unsafe_allow_html=True)
if st.button("⚡ CONSUMO DE ENERGÍA", use_container_width=True):
    ir_a("energia")
    st.rerun()

# 5. Imanes decorativos de alimentos al pie de la puerta
st.markdown("""
<div class="fridge-magnets-footer">
    🧊 🧀 🥕 🍋 🫐 🥛
</div>
""", unsafe_allow_html=True)
