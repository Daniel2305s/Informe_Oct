import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import re

# ==============================
# 🌸 Apariencia personalizada
# ==============================
st.markdown("""
    <style>
        .reportview-container { font-family: 'Montserrat', sans-serif; }
        h1, h2 { color: #e72380; }
        body { background-color: #fff; }
        .sidebar .sidebar-content { background-color: #ed6da6; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Informe de Ventas")

# ==============================
# 📥 Cargar datos desde Google Sheets
# ==============================
SHEET_ID = "1HLsdLZW_uihIRGl1tP7ehZwRUTuDXtDUz_FTNkcA1hA"
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid=0"

@st.cache_data
def cargar_datos(url):
    df = pd.read_csv(url)
    # Normalizamos nombres de columnas para evitar espacios
    df.columns = df.columns.str.strip()
    return df

df = cargar_datos(csv_url)

# ==============================
# 🧮 Preprocesamiento de datos
# ==============================
# Extraer la cantidad numérica del inicio de la columna "Producto(s)"
def extraer_cantidad(texto):
    match = re.match(r"(\d+)[×x]", str(texto).strip())
    if match:
        return int(match.group(1))
    return 1  # Si no hay número explícito, asumimos 1 unidad

df['Cantidad'] = df['Producto(s)'].apply(extraer_cantidad)

# Filtrar ventas completadas y devueltas
ventas_completadas = df[df['Estado'].str.lower() == 'completed']
ventas_devueltas = df[df['Estado'].str.lower() == 'refunded']

# ==============================
# 📌 Métricas principales
# ==============================
total_ventas_exitosas = ventas_completadas.shape[0]
total_ventas_devueltas = ventas_devueltas.shape[0]
total_productos_vendidos = ventas_completadas['Cantidad'].sum()
total_dinero = ventas_completadas['Ventas netas'].replace('[\$,]', '', regex=True).astype(float).sum()

# ==============================
# 🏆 Top Producto / Origen / Pago
# ==============================
producto_top = (ventas_completadas.groupby('Producto(s)')['Cantidad']
                .sum().nlargest(1).index[0])

origen_top = (ventas_completadas.groupby('atribucion')['Cantidad']
              .sum().nlargest(1).index[0])

pago_top = (ventas_completadas.groupby('pago')['Cantidad']
            .sum().nlargest(1).index[0])

# ==============================
# 📊 Mostrar métricas en Streamlit
# ==============================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas exitosas", total_ventas_exitosas)
col2.metric("Ventas devueltas", total_ventas_devueltas)
col3.metric("Productos vendidos", int(total_productos_vendidos))
col4.metric("Total dinero", f"${total_dinero:,.2f}")

st.subheader(f"🏆 Producto más vendido: {producto_top}")
st.subheader(f"📈 Origen con más ventas: {origen_top}")
st.subheader(f"💳 Método de pago más usado: {pago_top}")

# ==============================
# 📈 Gráficos
# ==============================
# Ventas por producto
fig, ax = plt.subplots(figsize=(10, 5))
ventas_completadas.groupby('Producto(s)')['Cantidad'].sum().sort_values(ascending=False).plot(
    kind='bar', color='#e72380', ax=ax
)
plt.title('Ventas por Producto')
plt.ylabel('Cantidad vendida')
plt.xticks(rotation=45, ha='right')
st.pyplot(fig)

# Ventas por método de pago
fig2, ax2 = plt.subplots(figsize=(7, 5))
ventas_completadas.groupby('pago')['Cantidad'].sum().plot(
    kind='bar', color='#ed6da6', ax=ax2
)
plt.title('Ventas por Método de Pago')
plt.ylabel('Cantidad vendida')
st.pyplot(fig2)
