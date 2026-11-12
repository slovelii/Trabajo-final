import streamlit as st

# Botón para regresar a la puerta principal de la nevera
if st.button("Volver al Panel Principal"):
    st.switch_page("Inicio.py") # Asegúrate de que coincida con el nombre de tu archivo raíz
