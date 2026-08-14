import streamlit as st
import pandas as pd
import json, math, os

# ================= EL "SERVICIO" =================
def haversine(lat1, lon1, lat2, lon2):
    """Distancia en km entre dos coordenadas (fórmula de Haversine)."""
    R = 6371.0
    dlat, dlon = math.radians(lat2-lat1), math.radians(lon2-lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

@st.cache_data
def cargar_estaciones():
    with open("estaciones.json", encoding="utf-8") as f:
        return json.load(f)

def estaciones_cercanas(lat, lon, limite):
    data = [dict(e) for e in cargar_estaciones()]
    for e in data:
        e["distancia_km"] = round(haversine(lat, lon, e["lat"], e["lon"]), 2)
    return sorted(data, key=lambda x: x["distancia_km"])[:limite]

# ================= LA PÁGINA WEB =================
st.set_page_config(page_title="Estaciones Cercanas", page_icon="🚓", layout="centered")

st.markdown("""
<div style="text-align:center; padding:2rem 1rem;
            background:linear-gradient(135deg,#1b3a6b,#2e6db4);
            border-radius:15px; color:white; margin-bottom:1.5rem;">
    <h1 style="color:white; margin:0;">🚓 Estaciones policiales más cercanas</h1>
    <p style="color:#ffd76e; font-weight:bold; margin:0.4rem 0;">By: Claudia Aguilar</p>
    <p style="color:#e8e8e8; margin:0.4rem 0;">
        Proyecto de Computación en la Nube.<br>
        Ingresa tus coordenadas y presiona <b>Buscar</b>.
    </p>
</div>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
lat = c1.number_input("Latitud",  value=15.7597, format="%.6f")
lon = c2.number_input("Longitud", value=-86.7822, format="%.6f")
limite = c3.number_input("Nº estaciones", 1, 10, 3)

if st.button("🔍 Buscar", type="primary"):
    res = estaciones_cercanas(lat, lon, limite)
    df  = pd.DataFrame(res)

    st.subheader("✅ Las más cercanas")
    for i, e in enumerate(res, 1):
        st.markdown(f"**{i}. {e['nombre']}** — a {e['distancia_km']} km de ti")

    st.dataframe(df[["nombre","lat","lon","distancia_km"]], use_container_width=True)

    st.subheader("️ Mapa")
    df_mapa = pd.concat([pd.DataFrame([{"lat": lat, "lon": lon}]), df[["lat","lon"]]])
    st.map(df_mapa)
