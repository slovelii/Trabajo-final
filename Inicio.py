import streamlit as st

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartFridge IoT 🧊 — Centro de Control",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 1. Definir las páginas secundarias de forma segura
# (Asegúrate de que tus archivos en la carpeta 'pages/' se llamen exactamente así y sin tildes)
energia_page = st.Page("pages/energia.py", title="Energía", icon="⚡")
inventario_page = st.Page("pages/inventario.py", title="Inventario", icon="📷")
temperatura_page = st.Page("pages/temperatura.py", title="Temperatura", icon="🌡️")

# Registrar la navegación global (esto evita que Streamlit colapse)
nav = st.navigation([energia_page, inventario_page, temperatura_page], position="hidden")

# ─────────────────────────────────────────────
# ESTILOS CSS: ESTÉTICA DIVERTIDA Y MODERNA
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%) !important;
    }

    .fridge-door {
        background: #ffffff;
        border: 6px solid #0284c7;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(2, 132, 199, 0.2);
        text-align: center;
        margin-bottom: 25px;
    }

    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
        100% { transform: translateY(0px); }
    }

    .animated-fridge {
        animation: float 4s ease-in-out infinite;
        font-size: 4rem;
        margin-bottom: 10px;
    }

    h1 {
        font-family: 'Fredoka', cursive !important;
        color: #0369a1 !important;
        font-size: 2.5rem !important;
    }

    p {
        color: #334155 !important;
        font-size: 1.1rem !important;
    }

    /* Estilo para los botones de enlace de página */
    [data-testid="stPageLink"] {
        background: #ffffff !important;
        border: 3px solid #0284c7 !important;
        border-radius: 16px !important;
        padding: 15px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        text-align: center;
    }

    [data-testid="stPageLink"]:hover {
        background: #0284c7 !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.4);
        border-color: #0369a1 !important;
    }
    
    [data-testid="stPageLink"] span {
        font-family: 'Fredoka', cursive !important;
        font-size: 1.2rem !important;
        color: #0369a1 !important;
    }

    [data-testid="stPageLink"]:hover span {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# INTERFAZ DE LA NEVERA VIRTUAL (HOME)
# ─────────────────────────────────────────────
st.markdown("""
<div class="fridge-door">
    <div class="animated-fridge">🧊🤖</div>
    <h1>SmartFridge Home</h1>
    <p>Tu asistente inteligente de cocina, inventario y conservación.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #0369a1; font-family: Fredoka;'>🎛️ Panel de Control de la Nevera</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Selecciona una sección para navegar directamente:</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.page_link(energia_page, label="⚡ Energía", use_container_width=True)

with col2:
    st.page_link(inventario_page, label="📷 Inventario", use_container_width=True)

with col3:
    st.page_link(temperatura_page, label="🌡️ Temperatura", use_container_width=True)
