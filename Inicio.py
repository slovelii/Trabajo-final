import streamlit as st
from pathlib import Path

# 1. Configuración de página (una sola vez en toda la app)
st.set_page_config(
    page_title="Panel de Control - Nevera Inteligente",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Localizador automático de tus archivos en /pages (resuelve rutas relativas reales)
BASE_DIR = Path(__file__).resolve().parent
PAGES_DIR = BASE_DIR / "pages"

def buscar_pagina(palabra_clave):
    """Busca el archivo real en /pages que contenga la palabra clave (ej. 'temperatura')."""
    if PAGES_DIR.exists():
        for archivo in PAGES_DIR.glob("*.py"):
            if palabra_clave.lower() in archivo.stem.lower():
                return str(archivo)
    return None

ruta_temp = buscar_pagina("temperatura")
ruta_inv = buscar_pagina("inventario")
ruta_ener = buscar_pagina("energia")

# 3. Vista de la puerta principal de la nevera
def vista_inicio():
    st.markdown("""
        <style>
        #MainMenu, footer, header {visibility: hidden;}
        [data-testid="stSidebar"], [data-testid="collapsedControl"] {display: none;}
        
        .stApp {
            background-color: #1e2226;
            font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
        }
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
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="brand-plate">SISTEMA DE CONTROL FRIGORÍFICO</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="led-screen">
            <div class="led-title">ESTADO DEL SISTEMA : OPERATIVO</div>
            <div class="led-metrics">
                <div>
                    <div class="metric-value">3.2°C</div>
                    <div class="metric-label">Refrigerador</div>
                </div>
                <div style="height: 40px; width: 1px; background-color: #263238;"></div>
                <div>
                    <div class="metric-value">-18.0°C</div>
                    <div class="metric-label">Congelador</div>
                </div>
                <div style="height: 40px; width: 1px; background-color: #263238;"></div>
                <div>
                    <div class="metric-value">ECO</div>
                    <div class="metric-label">Modo Energía</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="door-seal"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Módulos de Monitoreo</div>', unsafe_allow_html=True)

    # Botones que usan los objetos st.Page registrados abajo
    if st.button("CONTROL DE TEMPERATURA", use_container_width=True):
        if pag_temperatura:
            st.switch_page(pag_temperatura)
        else:
            st.error(f"No se encontró el archivo de temperatura en: {PAGES_DIR}")

    if st.button("GESTIÓN DE INVENTARIO", use_container_width=True):
        if pag_inventario:
            st.switch_page(pag_inventario)
        else:
            st.error(f"No se encontró el archivo de inventario en: {PAGES_DIR}")

    if st.button("CONSUMO DE ENERGÍA", use_container_width=True):
        if pag_energia:
            st.switch_page(pag_energia)
        else:
            st.error(f"No se encontró el archivo de energía en: {PAGES_DIR}")

# 4. Registro dinámico de páginas en st.navigation
pag_inicio = st.Page(vista_inicio, title="Panel Principal", default=True)
paginas_registradas = [pag_inicio]

pag_temperatura = st.Page(ruta_temp, title="Temperatura") if ruta_temp else None
if pag_temperatura:
    paginas_registradas.append(pag_temperatura)

pag_inventario = st.Page(ruta_inv, title="Inventario") if ruta_inv else None
if pag_inventario:
    paginas_registradas.append(pag_inventario)

pag_energia = st.Page(ruta_ener, title="Energía") if ruta_ener else None
if pag_energia:
    paginas_registradas.append(pag_energia)

# 5. Ejecutar navegación ocultando el menú lateral nativo
pg = st.navigation(paginas_registradas, position="hidden")
pg.run()
