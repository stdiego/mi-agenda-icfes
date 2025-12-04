import streamlit as st
from supabase import create_client
from datetime import datetime

# ======================================
# CONFIGURACIÓN STREAMLIT
# ======================================
st.set_page_config(page_title="Agenda Clases ICFES", page_icon="📚", layout="centered")

st.title("📚 Agenda de Clases Personalizadas ICFES")
st.write("Reserva tu clase seleccionando tema, fecha y hora.")


# ======================================
# CONEXIÓN A SUPABASE
# ======================================
SUPABASE_URL = "https://wedibjoowpxlhwvseqae.supabase.co"
SUPABASE_KEY = "sb_publishable_uQcIW11w4VC9QN3YJFoGdw_hxYUWGFD"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ======================================
# DATOS DEL SISTEMA
# ======================================
TEMAS = [
    "Matemáticas",
    "Lectura crítica",
    "Sociales",
    "Ciencias naturales",
    "Inglés",
    "Razonamiento lógico",
]

HORAS = ["08:00", "10:00", "14:00", "16:00", "18:00"]


# ======================================
# FORMULARIO DE RESERVA
# ======================================
with st.form("form_reserva"):
    nombre = st.text_input("👤 Nombre del estudiante")
    tema = st.selectbox("📘 Tema a estudiar", TEMAS)
    fecha = st.date_input("📅 Fecha", min_value=datetime.today())
    hora = st.selectbox("⏰ Hora", HORAS)

    enviar = st.form_submit_button("Agendar Clase")


# ======================================
# PROCESAR RESERVA
# ======================================
if enviar:
    # 1. Verificar si la hora ya está ocupada
    consulta = supabase.table("reservas").select("*").eq("fecha", str(fecha)).eq("hora", hora).execute()

    if len(consulta.data) > 0:
        st.error("⚠️ Esa hora ya está reservada. Elige otra.")
    else:
        # 2. Insertar en Supabase
        supabase.table("reservas").insert({
            "nombre_estudiante": nombre,
            "tema": tema,
            "fecha": str(fecha),
            "hora": hora
        }).execute()

        st.success("✅ Clase agendada con éxito.")


# ======================================
# MOSTRAR RESERVAS EXISTENTES
# ======================================
st.subheader("📋 Clases Programadas")

reservas = supabase.table("reservas").select("*").order("fecha").order("hora").execute()
df = reservas.data

st.dataframe(df)
