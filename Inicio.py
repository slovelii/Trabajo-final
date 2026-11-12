import streamlit as st
from pathlib import Path

# Configuración inicial de la página
st.set_page_config(
    page_title="Panel de Control - Nevera Inteligente",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Controlador de navegación en memoria (evita StreamlitPageNotFoundError)
if "pagina_activa" not in st.session_state:
    st.session_state.pagina_activa = "inicio"

def ir_a(nombre_pagina):
    st.session_state.pagina_activa = nombre_pagina

# Si el usuario seleccionó uno de los 3 módulos, cargamos ese archivo directamente
if st.session_state.pagina_activa != "inicio":
    # Ocultar barra lateral también en las subpáginas
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # Botón universal para regresar a la puerta de la nevera
    if st.button("← Volver al Panel Principal"):
        st.session_state.pagina_activa = "inicio"
        st.rerun()

    # Ruta exacta hacia el archivo dentro de la carpeta pages/
    ruta_archivo = Path(__file__).parent / "pages" / f"{st.session_state.pagina_activa}.py"

    if ruta_archivo.exists():
        codigo = ruta_archivo.read_text(encoding="utf-8")
        # Ignoramos set_page_config o switch_page viejos dentro del archivo secundario para que no choquen
        lineas_limpias = []
        for linea in codigo.splitlines():
            if "st.switch_page" in linea:
                lineas_limpias.append(linea.replace("st.switch_page", "# st.switch_page"))
            else:
                lineas_limpias.append(linea)
        exec("\n".join(lineas_limpias), globals())
    else:
        st.error(f"No se encontró el archivo: {ruta_archivo}")

    st.stop()

# =====================================================================
# DE AQUÍ EN ADELANTE ES TU INTERFAZ DE INICIO EXACTA
# =====================================================================

st.markdown("""
    <style>
    /* Ocultar elementos nativos de Streamlit (menú, footer, header y barra lateral) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
    
    /* Fondo general de la página (ambiente exterior) */
    .stApp {
        background-color: #1e2226;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }

    /* Contenedor principal que simula el cuerpo de acero inoxidable de la nevera */
    .main .block-container {
        background: linear-gradient(135deg, #d8dee3 0%, #b8c2cc 50%, #9aa6b2 100%);
        border-radius: 28px;
        border: 8px solid #6c7680;
        box-shadow: 
            inset 0 0 25px rgba(255, 255, 255, 0.6),
            0 25px 50px rgba(0, 0, 0, 0.7);
        padding: 2.5rem 2.5rem 3.5rem 2.5rem;
        max-width: 580px;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }

    /* Marco superior e identidad de marca (estilo placa metálica) */
    .brand-plate {
        text-align: center;
        color: #3b4249;
        font-weight: 800;
        letter-spacing: 5px;
        font-size: 0.9rem;
        text-transform: uppercase;
        margin-bottom: 1.5rem;
        text-shadow: 0 1px 1px rgba(255,255,255,0.8);
    }

    /* Pantalla digital empotrada (Hub de estado) */
    .led-screen {
        background-color: #0d1217;
        border: 4px solid #454d55;
        border-radius: 14px;
        padding: 22px;
        color: #00e5ff;
        text-align: center;
        box-shadow: inset 0 0 18px rgba(0, 229, 255, 0.15);
        margin-bottom: 25px;
    }

    .led-title {
        font-size: 0.75rem;
        color: #6c8090;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .led-metrics {
        display: flex;
        justify-content: space-around;
        align-items: center;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 10px;
    }

    .metric-box {
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #e0f7fa;
        text-shadow: 0 0 8px rgba(0, 229, 255, 0.5);
    }

    .metric-label {
        font-size: 0.7rem;
        color: #4dd0e1;
        text-transform: uppercase;
    }

    /* División física entre la puerta superior y la inferior */
    .door-seal {
        height: 10px;
        background: #2b3035;
        margin: 30px -2.5rem;
        border-top: 2px solid #555e67;
        border-bottom: 2px solid #16191c;
        box-shadow: 0 3px 6px rgba(0,0,0,0.3);
    }

    .section-label {
        color: #2c333a;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 12px;
        text-align: center;
    }

    /* Estilización de los botones de Streamlit para que parezcan paneles táctiles físicos */
    div.stButton > button {
        width: 100%;
        height: 75px;
        background: linear-gradient(180deg, #2b333c 0%, #1c2228 100%);
        color: #e2e8f0;
        border: 2px solid #4a5568;
        border-radius: 12px;
        font-size: 1rem;
        font-weight: 600;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25), inset 0 1px 1px rgba(255,255,255,0.1);
        margin-bottom: 12px;
    }

    div.stButton > button:hover {
        background: linear-gradient(180deg, #323c47 0%, #232a31 100%);
        border-color: #00e5ff;
        color: #00e5ff;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.25);
        transform: translateY(-1px);
    }

    div.stButton > button:active {
        transform: translateY(2px);
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
    }
    </style>
""", unsafe_allow_html=True)

# 1. Placa de marca superior
st.markdown('<div class="brand-plate">SISTEMA DE CONTROL FRIGORÍFICO</div>', unsafe_allow_html=True)

# 2. Pantalla LED de estado general (Puerta Superior)
st.markdown("""
    <div class="led-screen">
        <div class="led-title">ESTADO DEL SISTEMA : OPERATIVO</div>
        <div class="led-metrics">
            <div class="metric-box">
                <div class="metric-value">3.2°C</div>
                <div class="metric-label">Refrigerador</div>
            </div>
            <div style="height: 40px; width: 1px; background-color: #263238;"></div>
            <div class="metric-box">
                <div class="metric-value">-18.0°C</div>
                <div class="metric-label">Congelador</div>
            </div>
            <div style="height: 40px; width: 1px; background-color: #263238;"></div>
            <div class="metric-box">
                <div class="metric-value">ECO</div>
                <div class="metric-label">Modo Energía</div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# 3. Sello divisor de puertas
st.markdown('<div class="door-seal"></div>', unsafe_allow_html=True)

# 4. Panel de navegación (Puerta Inferior)
st.markdown('<div class="section-label">Módulos de Monitoreo</div>', unsafe_allow_html=True)

# Botones de navegación sin usar st.switch_page
if st.button("CONTROL DE TEMPERATURA", use_container_width=True):
    ir_a("temperatura")
    st.rerun()

if st.button("GESTIÓN DE INVENTARIO", use_container_width=True):
    ir_a("inventario")
    st.rerun()

if st.button("CONSUMO DE ENERGÍA", use_container_width=True):
    ir_a("energia")
    st.rerun()
