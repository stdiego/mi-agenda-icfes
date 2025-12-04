import streamlit as st
import pandas as pd
from datetime import datetime

# ======================================
# CONFIGURACIÓN GENERAL
# ======================================
st.set_page_config(
    page_title="Agenda Clases ICFES",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Agenda de Clases Personalizadas ICFES")
st.write("Selecciona tema, fecha y hora para agendar tu clase.")

# ======================================
# BASE DE DATOS TEMPORAL
# (En versión profesional → PostgreSQL o Google Sheets)
# ======================================
if "reservas" not in st.session_state:
    st.session_state["reservas"] = pd.DataFrame(
        columns=["nombre", "tema", "fecha", "hora"]
    )

TEMAS = [
    "Matemáticas",
    "Lectura crítica",
    "Sociales",
    "Ciencias naturales",
    "Inglés",
    "Razonamiento lógico"
]

HORAS = ["08:00", "10:00", "14:00", "16:00", "18:00"]


# ======================================
# FORMULARIO DE RESERVA
# ======================================
with st.form("reserva_form"):
    nombre = st.text_input("👤 Nombre del estudiante")

    tema = st.selectbox("📘 Tema a estudiar", TEMAS)

    fecha = st.date_input("📅 Fecha", min_value=datetime.today())

    hora = st.selectbox("⏰ Hora", HORAS)

    enviar = st.form_submit_button("Agendar clase")

# ======================================
# PROCESO DE RESERVA
# ======================================
if enviar:
    df = st.session_state["reservas"]

    # Validar si la hora ya está ocupada
    existe = df[
        (df["fecha"] == str(fecha)) &
        (df["hora"] == hora)
    ]

    if not existe.empty:
        st.error("⚠️ Esa hora ya está reservada. Por favor elige otra.")
    else:
        nueva = pd.DataFrame(
            [{
                "nombre": nombre,
                "tema": tema,
                "fecha": str(fecha),
                "hora": hora
            }]
        )

        st.session_state["reservas"] = pd.concat(
            [df, nueva], ignore_index=True
        )

        st.success("✅ Clase agendada con éxito.")


# ======================================
# LISTA DE RESERVAS
# ======================================
st.subheader("📋 Clases Programadas")
st.dataframe(st.session_state["reservas"])
