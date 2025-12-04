import streamlit as st
from supabase import create_client, Client
from datetime import datetime

# ==========================
# CONFIG STREAMLIT
# ==========================
st.set_page_config(page_title="Agenda ICFES", page_icon="📚", layout="centered")

st.title("📚 Agenda de Clases Personalizadas ICFES")

# ==========================
# CONEXIÓN A SUPABASE
# ==========================
SUPABASE_URL = "https://wedibjoowpxlhwvseqae.supabase.co"
SUPABASE_KEY = "sb_publishable_uQcIW11w4VC9QN3YJFoGdw_hxYUWGFD"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================
# DATOS DEL FORMULARIO
# ==========================
TEMAS = [
    "Matemáticas",
    "Lectura crítica",
    "Sociales",
    "Ciencias naturales",
    "Inglés",
    "Razonamiento lógico",
]

HORAS = ["08:00", "10:00", "14:00", "16:00", "18:00"]

# ==========================
# FORMULARIO
# ==========================
with st.form("reserva_form"):
    nombre = st.text_input("👤 Nombre del estudiante")
    tema = st.selectbox("📘 Tema", TEMAS)
    fecha = st.date_input("📅 Fecha", min_value=datetime.today())
    hora = st.selectbox("⏰ Hora", HORAS)

    enviar = st.form_submit_button("Agendar")

if enviar:
    # Verificar que la hora esté disponible
    result = supabase.table("reservas").select("*").eq("fecha", str(fecha)).eq("hora", hora).execute()

    if result.data:
        st.error("⚠️ Esa hora ya está reservada.")
    else:
        supabase.table("reservas").insert({
            "nombre_estudiante": nombre,
            "tema": tema,
            "fecha": str(fecha),
            "hora": hora
        }).execute()

        st.success("✅ Clase agendada con éxito.")

# Mostrar reservas
st.subheader("📋 Clases Programadas")
reservas = supabase.table("reservas").select("*").order("fecha").order("hora").execute()

if reservas.data:
    st.dataframe(reservas.data)
else:
    st.info("Aún no hay reservas.")
