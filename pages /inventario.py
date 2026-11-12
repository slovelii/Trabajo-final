import streamlit as st

if st.button("Volver al Panel Principal"):
    st.switch_page(st.session_state["pag_inicio"])
