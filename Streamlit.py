import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================
# 🎨 Apariencia personalizada
# ==========================
st.markdown("""
    <style>
        .reportview-container { font-family: 'Montserrat', sans-serif; }
        h1, h2, h3 { color: #e72380; }
        body { background-color: #fff; }
        .sidebar .sidebar-content { background-color: #ed6da6; }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Informe de Ventas")

# ==========================
# 📥 Cargar datos desde Google Sheets
# ==========================
SHEET_ID = "1HLsdLZW_uihIRGl1tP7ehZwRUTuDXtDUz_FTNkcA1hA"
GID = "0"  # ID de la pestaña en Google Sheets
csv_url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data
def cargar_datos(url: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(url)
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return pd.DataFrame()

df = cargar_datos(csv_url)

# Verificación de datos cargados
if df.empty:
    st.error("⚠️ No se pudieron cargar los datos. Verifica la URL o los permisos de la hoja.")
    st.stop()

# Normalizar nombres de columnas
df.columns = df.columns.str.strip().str.lower()

# ==========================
# 📈 Cálculo de métricas
# ==========================
if 'estado' not in df.columns:
    st.error("❌ La columna 'estado' no existe en el archivo. Revisa el nombre exacto en Google Sheets.")
    st.stop()

ventas_completadas = df[df['estado'] == 'completed']
ventas_devueltas = df[df['estado'] == 'refunded']

ventas_exitosas = ventas_completadas.shape[0]
ventas_refund = ventas_devueltas.shape[0]
total_productos = ventas_completadas['cantidad'].sum() if 'cantidad' in df.columns else 0
total_dinero = ventas_completadas['total'].sum() if 'total' in df.columns else 0

# Top producto, atribución y pago
def obtener_top(df, columna):
    if columna in df.columns and not df.empty:
        return df.groupby(columna)['cantidad'].sum().nlargest(1).index[0]
    return "No disponible"

producto_top = obtener_top(ventas_completadas, 'producto')
origen_top = obtener_top(ventas_completadas, 'atribucion')
pago_top = obtener_top(ventas_completadas, 'pago')

# ==========================
# 🧾 Mostrar métricas
# ==========================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Ventas exitosas", ventas_exitosas)
col2.metric("Ventas devueltas", ventas_refund)
col3.metric("Total productos vendidos", int(total_productos))
col4.metric("Total dinero", f"${total_dinero:,.2f}")

st.subheader(f"🏆 Producto más vendido: {producto_top}")
st.subheader(f"🌐 Origen de atribución con más ventas: {origen_top}")
st.subheader(f"💳 Método de pago más usado: {pago_top}")

# ==========================
# 📊 Gráficos
# ==========================
if 'producto' in df.columns and 'cantidad' in df.columns and not ventas_completadas.empty:
    fig, ax = plt.subplots()
    ventas_completadas.groupby('producto')['cantidad'].sum().plot(
        kind='bar', color='#e72380', ax=ax)
    ax.set_title('Ventas por producto')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)

if 'pago' in df.columns and 'cantidad' in df.columns and not ventas_completadas.empty:
    fig2, ax2 = plt.subplots()
    ventas_completadas.groupby('pago')['cantidad'].sum().plot(
        kind='bar', color='#ed6da6', ax=ax2)
    ax2.set_title('Ventas por método de pago')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)

# ==========================
# 📝 Nota final
# ==========================
st.markdown("---")
st.caption("Datos obtenidos en tiempo real desde Google Sheets.")
