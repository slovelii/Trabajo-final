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
# INTERFAZ DE INICIO TEMATIZADA COMO NEVERA COLORIDA Y DIVERTIDA
# =====================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@500;600;700&family=Nunito:wght@600;700;800&display=swap');

/* Ocultar elementos nativos de Streamlit (menú, footer, header y barra lateral) */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}

/* Fondo de cocina alegre con patrón suave de azulejos */
.stApp {
    background-color: #FFF8EC;
    background-image:
        linear-gradient(90deg, rgba(255, 190, 152, 0.16) 1px, transparent 1px),
        linear-gradient(rgba(255, 190, 152, 0.16) 1px, transparent 1px),
        radial-gradient(circle at 15% 15%, rgba(114, 239, 221, 0.35), transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(255, 173, 173, 0.35), transparent 45%);
    background-size: 36px 36px, 36px 36px, 100% 100%, 100% 100%;
    font-family: 'Nunito', sans-serif;
}

/* Cuerpo de la nevera estilo retro pastel (compatible con varias versiones de Streamlit) */
.main .block-container,
[data-testid="stMainBlockContainer"] {
    background: linear-gradient(165deg, #A8F9FF 0%, #72EFDD 42%, #56CFE1 100%);
    border-radius: 44px;
    border: 9px solid #FFFFFF;
    outline: 5px solid #48BFE3;
    box-shadow:
        inset 10px 10px 25px rgba(255, 255, 255, 0.7),
        inset -10px -12px 24px rgba(0, 119, 182, 0.22),
        0 26px 55px rgba(27, 73, 101, 0.28);
    padding: 2rem 2.2rem 2.5rem 2.2rem !important;
    max-width: 590px !important;
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
}

/* Fila superior de imanes y placa retro de marca */
.fridge-top-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.1rem;
    gap: 8px;
}

.magnet-pill {
    background: #FFFFFF;
    border-radius: 50%;
    width: 42px;
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.35rem;
    box-shadow: 0 4px 0 rgba(0, 119, 182, 0.2), 0 6px 12px rgba(0,0,0,0.12);
    border: 3px solid #FFF3B0;
    user-select: none;
}

.mag-left { transform: rotate(-12deg); }
.mag-right { transform: rotate(12deg); border-color: #FFD6E0; }

.brand-plate {
    background: linear-gradient(180deg, #FFFFFF 0%, #F1F5F9 100%);
    border: 3px solid #FF6B6B;
    border-radius: 999px;
    padding: 8px 22px;
    text-align: center;
    color: #FF4D6D;
    font-family: 'Fredoka', cursive, sans-serif;
    font-weight: 700;
    letter-spacing: 1.5px;
    font-size: 1.15rem;
    text-transform: uppercase;
    box-shadow: 0 5px 0 #E05263, 0 8px 16px rgba(255, 77, 109, 0.2);
}

/* Pantalla inteligente colorida empotrada en la puerta superior */
.led-screen {
    background: linear-gradient(145deg, #1E1B4B 0%, #312E81 60%, #1E293B 100%);
    border: 5px solid #FFD166;
    border-radius: 24px;
    padding: 18px 16px 20px 16px;
    text-align: center;
    box-shadow:
        0 8px 0 rgba(217, 119, 6, 0.45),
        inset 0 0 22px rgba(56, 189, 248, 0.25);
    margin-bottom: 16px;
}

.led-title {
    display: inline-block;
    background: rgba(163, 230, 53, 0.18);
    border: 1.5px solid #A3E635;
    color: #D9F99D;
    border-radius: 999px;
    padding: 4px 14px;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.85rem;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 14px;
}

.led-metrics {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 10px;
    flex-wrap: wrap;
}

.metric-box {
    flex: 1;
    min-width: 115px;
    border-radius: 18px;
    padding: 12px 8px;
    text-align: center;
}

.metric-fridge {
    background: linear-gradient(180deg, rgba(56, 189, 248, 0.25), rgba(14, 165, 233, 0.15));
    border: 2px solid #38BDF8;
}

.metric-freezer {
    background: linear-gradient(180deg, rgba(165, 243, 252, 0.25), rgba(129, 140, 248, 0.2));
    border: 2px solid #A5F3FC;
}

.metric-eco {
    background: linear-gradient(180deg, rgba(163, 230, 53, 0.25), rgba(34, 197, 94, 0.18));
    border: 2px solid #A3E635;
}

.metric-icon {
    font-size: 1.35rem;
    margin-bottom: 2px;
}

.metric-value {
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 1.85rem;
    font-weight: 700;
    line-height: 1.1;
}

.metric-fridge .metric-value { color: #7DD3FC; }
.metric-freezer .metric-value { color: #E0F2FE; }
.metric-eco .metric-value { color: #BEF264; }

.metric-label {
    font-family: 'Nunito', sans-serif;
    font-size: 0.72rem;
    font-weight: 800;
    color: #F8FAFC;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-top: 4px;
}

/* Ventana divertida de zonas de comida y temperatura */
.food-zones {
    display: flex;
    justify-content: space-between;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}

.zone-chip {
    flex: 1;
    min-width: 135px;
    background: rgba(255, 255, 255, 0.88);
    border-radius: 16px;
    padding: 8px 10px;
    text-align: center;
    box-shadow: 0 4px 0 rgba(0, 119, 182, 0.16);
    border: 2px solid #FFFFFF;
}

.zone-foods {
    font-size: 1.15rem;
    letter-spacing: 3px;
}

.zone-name {
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    margin-top: 2px;
}

.zone-cold .zone-name { color: #0284C7; }
.zone-fresh .zone-name { color: #EA580C; }
.zone-veggie .zone-name { color: #16A34A; }

/* Sello divisor entre la puerta del congelador y la puerta principal + manija cromada */
.door-seal-wrap {
    position: relative;
    margin: 26px -2.2rem 22px -2.2rem;
}

.door-seal {
    height: 14px;
    background: linear-gradient(180deg, #0077B6 0%, #023E8A 50%, #0096C7 100%);
    border-top: 3px solid rgba(255, 255, 255, 0.75);
    border-bottom: 3px solid rgba(255, 255, 255, 0.45);
    box-shadow: 0 4px 8px rgba(2, 62, 138, 0.25);
}

.fridge-handle {
    width: 140px;
    height: 18px;
    background: linear-gradient(180deg, #FFFFFF 0%, #E2E8F0 55%, #CBD5E1 100%);
    border: 2px solid #94A3B8;
    border-radius: 999px;
    margin: 10px auto 0 auto;
    box-shadow: 0 5px 10px rgba(15, 23, 42, 0.2), inset 0 2px 3px #FFFFFF;
}

/* Nota adhesiva amarilla (Post-it) pegada a la puerta */
.sticky-note {
    background: linear-gradient(180deg, #FFF3B0 0%, #FFE66D 100%);
    color: #5C4700;
    border-radius: 16px 16px 26px 16px;
    padding: 13px 18px;
    margin: 0 auto 20px auto;
    max-width: 94%;
    text-align: center;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 1rem;
    font-weight: 600;
    box-shadow: 0 6px 0 rgba(217, 119, 6, 0.25), 0 10px 18px rgba(0, 0, 0, 0.12);
    transform: rotate(-1deg);
    position: relative;
    border: 2px solid #FFF9DB;
}

.sticky-pin {
    display: inline-block;
    width: 16px;
    height: 16px;
    background: radial-gradient(circle at 35% 35%, #FF8FA3, #E63946);
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    margin-bottom: 4px;
}

.section-label {
    color: #0F4C5C;
    font-family: 'Fredoka', cursive, sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 14px;
    text-align: center;
    text-shadow: 0 2px 0 rgba(255, 255, 255, 0.65);
}

/* Ocultar los marcadores invisibles para colorear cada botón individualmente */
[data-testid="stVerticalBlock"] > div:has(.btn-marker),
[data-testid="stElementContainer"]:has(.btn-marker),
.element-container:has(.btn-marker) {
    display: none !important;
}

/* Estilo base juguetón y táctil para los botones de Streamlit */
div.stButton > button,
[data-testid="stButton"] > button {
    width: 100%;
    height: 76px;
    background: linear-gradient(180deg, #FF6B6B 0%, #FF8E53 100%);
    color: #FFFFFF !important;
    border: 4px solid #FFFFFF !important;
    border-radius: 22px !important;
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    letter-spacing: 1px;
    text-transform: uppercase;
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
    box-shadow: 0 8px 0 rgba(15, 23, 42, 0.22), 0 12px 20px rgba(0, 0, 0, 0.16);
    margin-bottom: 10px;
}

div.stButton > button p,
[data-testid="stButton"] > button p {
    font-family: 'Fredoka', cursive, sans-serif !important;
    font-size: 1.18rem !important;
    font-weight: 700 !important;
    color: #FFFFFF !important;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.22);
    margin: 0 !important;
}

div.stButton > button:hover,
[data-testid="stButton"] > button:hover {
    transform: translateY(-3px) scale(1.015);
    filter: brightness(1.06);
    border-color: #FFF3B0 !important;
    box-shadow: 0 11px 0 rgba(15, 23, 42, 0.22), 0 16px 24px rgba(0, 0, 0, 0.2);
}

div.stButton > button:active,
[data-testid="stButton"] > button:active {
    transform: translateY(4px) scale(0.99);
    box-shadow: 0 3px 0 rgba(15, 23, 42, 0.25), 0 5px 10px rgba(0, 0, 0, 0.15);
}

/* Botón 1: Control de Temperatura (Azul Hielo / Frío) */
[data-testid="stVerticalBlock"] > div:has(.marker-temp) + div button,
[data-testid="stElementContainer"]:has(.marker-temp) + [data-testid="stElementContainer"] button,
.element-container:has(.marker-temp) + .element-container button {
    background: linear-gradient(135deg, #00B4D8 0%, #0077B6 100%) !important;
    box-shadow: 0 8px 0 #023E8A, 0 12px 20px rgba(2, 62, 138, 0.28) !important;
}

/* Botón 2: Gestión de Inventario (Fresa / Naranja Comida) */
[data-testid="stVerticalBlock"] > div:has(.marker-inv) + div button,
[data-testid="stElementContainer"]:has(.marker-inv) + [data-testid="stElementContainer"] button,
.element-container:has(.marker-inv) + .element-container button {
    background: linear-gradient(135deg, #FF595E 0%, #FF924C 100%) !important;
    box-shadow: 0 8px 0 #C83E37, 0 12px 20px rgba(200, 62, 55, 0.28) !important;
}

/* Botón 3: Consumo de Energía (Verde Eco / Limón) */
[data-testid="stVerticalBlock"] > div:has(.marker-eco) + div button,
[data-testid="stElementContainer"]:has(.marker-eco) + [data-testid="stElementContainer"] button,
.element-container:has(.marker-eco) + .element-container button {
    background: linear-gradient(135deg, #52B788 0%, #2D936C 100%) !important;
    box-shadow: 0 8px 0 #1B5E42, 0 12px 20px rgba(27, 94, 66, 0.28) !important;
}

/* Barra inferior de imanes decorativos de comida */
.fridge-magnets-footer {
    margin-top: 16px;
    background: rgba(255, 255, 255, 0.55);
    border: 2px dashed rgba(255, 255, 255, 0.9);
    border-radius: 20px;
    padding: 10px 14px;
    text-align: center;
    font-size: 1.45rem;
    letter-spacing: 10px;
    user-select: none;
}
</style>
""", unsafe_allow_html=True)

# 1. Placa de marca superior con imanes divertidos
st.markdown("""
<div class="fridge-top-bar">
    <div class="magnet-pill mag-left">🍓</div>
    <div class="brand-plate">❄️ MI NEVERA PLAY 🍎</div>
    <div class="magnet-pill mag-right">🍦</div>
</div>
""", unsafe_allow_html=True)

# 2. Pantalla LED colorida de estado general (Puerta Superior)
st.markdown("""
<div class="led-screen">
    <div class="led-title">✨ ESTADO: ¡FRESCA Y LISTA PARA JUGAR! ✨</div>
    <div class="led-metrics">
        <div class="metric-box metric-fridge">
            <div class="metric-icon">🥛🥬</div>
            <div class="metric-value">3.2°C</div>
            <div class="metric-label">Refrigerador</div>
        </div>
        <div class="metric-box metric-freezer">
            <div class="metric-icon">❄️🧊</div>
            <div class="metric-value">-18.0°C</div>
            <div class="metric-label">Congelador</div>
        </div>
        <div class="metric-box metric-eco">
            <div class="metric-icon">⚡🌿</div>
            <div class="metric-value">ECO</div>
            <div class="metric-label">Modo Energía</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# 3. Tarjetitas de colores, comidas y temperaturas de la nevera
st.markdown("""
<div class="food-zones">
    <div class="zone-chip zone-cold">
        <div class="zone-foods">🍦🧊🫐</div>
        <div class="zone-name">Congelados • -18°C</div>
    </div>
    <div class="zone-chip zone-fresh">
        <div class="zone-foods">🥛🧀🧃</div>
        <div class="zone-name">Lácteos • 3.2°C</div>
    </div>
    <div class="zone-chip zone-veggie">
        <div class="zone-foods">🍓🥑🥕</div>
        <div class="zone-name">Frescos • 5.0°C</div>
    </div>
</div>
""", unsafe_allow_html=True)

# 4. Sello divisor de puertas y manija retro
st.markdown("""
<div class="door-seal-wrap">
    <div class="door-seal"></div>
    <div class="fridge-handle"></div>
</div>
""", unsafe_allow_html=True)

# 5. Nota adhesiva divertida + Panel de navegación (Puerta Inferior)
st.markdown("""
<div class="sticky-note">
    <div class="sticky-pin"></div><br>
    🎮 ¡Toca un botón y juega con tu nevera! Elige qué quieres controlar hoy
</div>
<div class="section-label">✨ Módulos de Monitoreo ✨</div>
""", unsafe_allow_html=True)

# Botones de navegación sin usar st.switch_page (funcionalidad intacta)
st.markdown('<div class="btn-marker marker-temp"></div>', unsafe_allow_html=True)
if st.button("❄️ CONTROL DE TEMPERATURA 🌡️", use_container_width=True):
    ir_a("temperatura")
    st.rerun()

st.markdown('<div class="btn-marker marker-inv"></div>', unsafe_allow_html=True)
if st.button("🍓 GESTIÓN DE INVENTARIO 🥑", use_container_width=True):
    ir_a("inventario")
    st.rerun()

st.markdown('<div class="btn-marker marker-eco"></div>', unsafe_allow_html=True)
if st.button("⚡ CONSUMO DE ENERGÍA 🌿", use_container_width=True):
    ir_a("energia")
    st.rerun()

# 6. Imanes decorativos al pie de la puerta
st.markdown("""
<div class="fridge-magnets-footer">
    🧊 🍊 🥦 🧀 🍉 🥛
</div>
""", unsafe_allow_html=True)
