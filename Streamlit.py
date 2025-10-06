import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Apariencia personalizada Streamlit
st.markdown("""
    <style>
        .reportview-container { font-family: 'Montserrat', sans-serif; }
        h1, h2 { color: #e72380; }
        body { background-color: #fff; }
        .sidebar .sidebar-content { background-color: #ed6da6; }
    </style>
""", unsafe_allow_html=True)

st.title("Informe de Ventas")

SHEET_ID = "1HLsdLZW_uihIRGl1tP7ehZwRUTuDXtDUz_FTNkcA1hA"
SHEET_NAME = "Base_web" # Cambia si es otro nombre de hoja
csv_url = f"https://docs.google.com/spreadsheets/d/{"1HLsdLZW_uihIRGl1tP7ehZwRUTuDXtDUz_FTNkcA1hA"}/gviz/tq?tqx=out:csv&sheet={"Hoja 1"}"

@st.cache_data
def cargar_datos(url):
    return pd.read_csv(url)

df = cargar_datos(csv_url)

# Métricas solicitadas
ventas_exitosas = df[df['estado'] == 'completed'].shape[0]
ventas_devueltas = df[df['estado'] == 'refunded'].shape[0]
total_productos = df[df['estado'] == 'completed']['cantidad'].sum()
total_dinero = df[df['estado'] == 'completed']['total'].sum()
producto_top = df[df['estado'] == 'completed'].groupby('producto')['cantidad'].sum().idxmax()
origen_top = df[df['estado'] == 'completed'].groupby('atribución')['cantidad'].sum().idxmax()
pago_top = df[df['estado'] == 'completed'].groupby('pago')['cantidad'].sum().idxmax()

st.metric("Ventas exitosas", ventas_exitosas)
st.metric("Ventas devueltas", ventas_devueltas)
st.metric("Total productos vendidos", int(total_productos))
st.metric("Total dinero", f"${total_dinero:,.2f}")

st.subheader(f"Producto más vendido: {producto_top}")
st.subheader(f"Origen de atribución con más ventas: {origen_top}")
st.subheader(f"Método de pago con más ventas: {pago_top}")

fig, ax = plt.subplots()
df[df['estado'] == 'completed'].groupby('producto')['cantidad'].sum().plot(
    kind='bar', color='#e72380', ax=ax)
plt.title('Ventas por producto')
st.pyplot(fig)

fig2, ax2 = plt.subplots()
df[df['estado'] == 'completed'].groupby('pago')['cantidad'].sum().plot(
    kind='bar', color='#ed6da6', ax=ax2)
plt.title('Ventas por método de pago')
st.pyplot(fig2)
