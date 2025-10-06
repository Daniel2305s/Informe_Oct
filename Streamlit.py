import streamlit as st
import pandas as pd
from babel.numbers import format_currency

# =========================
# CONFIGURACIÓN DE LA PÁGINA
# =========================
st.set_page_config(
    page_title="Informe de Ventas",
    page_icon="📊",
    layout="wide"
)

# =========================
# CARGAR DATOS DESDE GOOGLE SHEETS
# =========================
sheet_url = "https://docs.google.com/spreadsheets/d/1HLsdLZW_uihIRGl1tP7ehZwRUTuDXtDUz_FTNkcA1hA/export?format=csv&gid=0"
df = pd.read_csv(sheet_url)

# Limpieza básica por si hay filas vacías
df = df.dropna(how='all')

# Asegurarse que las columnas numéricas estén en el tipo correcto
df['Cantidad'] = pd.to_numeric(df['Cantidad'], errors='coerce').fillna(0)
df['Total'] = pd.to_numeric(df['Total'], errors='coerce').fillna(0)

# =========================
# TÍTULO
# =========================
st.markdown("## 📊 **Informe de Ventas**")

# =========================
# MÉTRICAS BÁSICAS
# =========================
ventas_exitosas = len(df[df['Estado'].str.lower() == 'exitosa'])
ventas_devueltas = len(df[df['Estado'].str.lower() == 'devuelta'])
productos_vendidos = int(df['Cantidad'].sum())
total_dinero = df['Total'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas exitosas", ventas_exitosas)
col2.metric("Ventas devueltas", ventas_devueltas)
col3.metric("Productos vendidos", productos_vendidos)
col4.markdown(
    f"<div style='font-size:20px; font-weight:bold;'>{format_currency(total_dinero, 'COP', locale='es_CO')}</div>",
    unsafe_allow_html=True
)

# =========================
# PRODUCTO MÁS VENDIDO
# =========================
producto_mas_vendido = (
    df.groupby('Producto')
    .agg({'Cantidad': 'sum'})
    .sort_values('Cantidad', ascending=False)
    .head(1)
    .reset_index()
)

if not producto_mas_vendido.empty:
    nombre_producto = producto_mas_vendido['Producto'][0]
    cantidad_producto = int(producto_mas_vendido['Cantidad'][0])
    st.markdown(
        f"🏆 **Producto más vendido:** {nombre_producto} ({cantidad_producto} unidades)"
    )

# =========================
# ORIGEN CON MÁS VENTAS
# =========================
origen_top = (
    df['Origen']
    .value_counts()
    .reset_index()
    .rename(columns={'index': 'Origen', 'Origen': 'Cantidad'})
)

if not origen_top.empty:
    origen_mas_ventas = origen_top.iloc[0]['Origen']
    st.markdown(f"📈 **Origen con más ventas:** {origen_mas_ventas}")

# =========================
# MÉTODO DE PAGO MÁS USADO
# =========================
metodo_pago = (
    df.groupby('Método de pago')
    .agg({'Total': 'sum', 'Número de venta': 'count'})
    .sort_values('Número de venta', ascending=False)
    .head(1)
    .reset_index()
)

if not metodo_pago.empty:
    metodo = metodo_pago['Método de pago'][0]
    total_metodo = metodo_pago['Total'][0]
    num_ventas_metodo = metodo_pago['Número de venta'][0]

    st.markdown(
        f"💳 **Método de pago más usado:** {metodo} — "
        f"Total: **{format_currency(total_metodo, 'COP', locale='es_CO')}**, "
        f"en **{num_ventas_metodo} ventas**"
    )
