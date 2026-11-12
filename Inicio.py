import streamlit as st
import time

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartFridge IoT 🧊 — Centro de Control",
    page_icon="🧊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# ESTILOS CSS: ESTÉTICA DIVERTIDA, MODERNA Y ANIMADA
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@400;600&family=Quicksand:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Quicksand', sans-serif !important;
    }

    /* Fondo general estilo cocina moderna / refrigerador pastel */
    .stApp {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 50%, #7dd3fc 100%) !important;
    }

    /* Contenedor principal estilo puerta de nevera elegante */
    .fridge-door {
        background: #ffffff;
        border: 6px solid #0284c7;
        border-radius: 24px;
        padding: 30px;
        box-shadow: 0 15px 35px rgba(2, 132, 199, 0.2);
        text-align: center;
        margin-bottom: 25px;
        position: relative;
    }

    /* Animación de flotación sutil para dar vida */
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

    /* Títulos principales */
    h1 {
        font-family: 'Fredoka', cursive !important;
        color: #0369a1 !important;
        font-size: 2.5rem !important;
    }

    p {
        color: #334155 !important;
        font-size: 1.1rem !important;
    }

    /* Tarjetas de opciones / botones grandes */
    .stButton button {
        background: #ffffff !important;
        border: 3px solid #0284c7 !important;
        border-radius: 16px !important;
        color: #0369a1 !important;
        font-family: 'Fredoka', cursive !important;
        font-size: 1.3rem !important;
        padding: 30px 10px !important;
        box-shadow: 0 6px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton button:hover {
        background: #0284c7 !important;
        color: #ffffff !important;
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(2, 132, 199, 0.4);
        border-color: #0369a1 !important;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ESTADO DE NAVEGACIÓN SIMULADA
# ─────────────────────────────────────────────
if 'section' not in st.session_state:
    st.session_state.section = "home"

# ─────────────────────────────────────────────
# INTERFAZ DE LA NEVERA VIRTUAL (HOME)
# ─────────────────────────────────────────────

# Panel visual interactivo de la nevera
st.markdown("""
<div class="fridge-door">
    <div class="animated-fridge">🧊🤖</div>
    <h1>SmartFridge Home</h1>
    <p>Tu asistente inteligente de cocina, inventario y conservación a un solo toque.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: #0369a1; font-family: Fredoka;'>🎛️ Panel de Control de la Nevera</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 30px;'>Selecciona una de las funciones principales para interactuar con tu electrodoméstico:</p>", unsafe_allow_html=True)

# Tres columnas para los tres botones principales pedidos
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("<div style='text-align: center;'>⚡</div>", unsafe_allow_html=True)
    if st.button("⚡\n\n Energía", use_container_width=True):
        st.session_state.section = "energia"
        st.toast("Cargando módulo de Energía...", icon="⚡")

with col2:
    st.markdown("<div style='text-align: center;'>📷</div>", unsafe_allow_html=True)
    if st.button("📷\n\n Inventario", use_container_width=True):
        st.session_state.section = "inventario"
        st.toast("Abriendo la cámara del refrigerador...", icon="📷")

with col3:
    st.markdown("<div style='text-align: center;'>🌡️</div>", unsafe_allow_html=True)
    if st.button("🌡️\n\n Temperatura", use_container_width=True):
        st.session_state.section = "temperatura"
        st.toast("Monitoreando sensores térmicos...", icon="🌡️")

# ─────────────────────────────────────────────
# MANEJO DE VISTAS SEGÚN LA SECCIÓN SELECCIONADA
# ─────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.session_state.section == "energia":
    st.info("🔌 **Módulo de Energía Seleccionado:** Aquí podrás prender, suspender y auditar el consumo eléctrico de tu nevera en tiempo real.")
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.section = "home"
        st.rerun()

elif st.session_state.section == "inventario":
    st.success("🍎 **Módulo de Inventario Seleccionado:** Aquí se conectará la cámara inteligente para auditar alimentos, detectar caducidades y sugerir compras.")
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.section = "home"
        st.rerun()

elif st.session_state.section == "temperatura":
    st.warning("❄️ **Módulo de Temperatura Seleccionado:** Aquí visualizarás las gráficas de frío, ajustarás los grados del congelador y recibirás alertas tempranas de fallas.")
    if st.button("⬅️ Volver al Panel Principal"):
        st.session_state.section = "home"
        st.rerun()
