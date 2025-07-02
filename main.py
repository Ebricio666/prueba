import streamlit as st
import pandas as pd
import numpy as np

# ========================================
# 🏷️ CONFIG
# ========================================
st.set_page_config(layout="wide")

st.title("📊 Reporte Gráfico de Municipios Normalizados")
st.markdown("""
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ========================================
# 🔗 LECTURA GOOGLE SHEET
# ========================================
# Reemplaza con tu enlace CSV correcto (público)
url_csv = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url_csv)

st.success("✅ Datos cargados correctamente desde Google Sheets.")
st.write(f"Registros: {len(df)}")

# ========================================
# 🧹 MUNICIPIO NORMALIZADO
# ========================================
# 1️⃣ Base en minúsculas y sin espacios extra
df['Municipio_Base'] = df['Municipio donde vive actualmente'].str.lower().str.strip()

# 2️⃣ Condiciones de agrupación
condiciones = [
    df['Municipio_Base'].str.contains(r'\bcolima\b|colima colima|colima\.colima|colima, colima|colima, cómala|colima,col|colima, esta semana villa de alvarez', na=False),
    df['Municipio_Base'].str.contains(r'villa.*álvarez|villa.*alvarez|villa dr alvarez|villa de alvares|villa de álvares', na=False),
    df['Municipio_Base'].str.contains(r'cuauht[eé]moc|cuahutemoc|cuauthemoc', na=False),
    df['Municipio_Base'].str.contains(r'comala|zacualpan|suchitlan', na=False),
    df['Municipio_Base'].str.contains(r'manzanillo|bahía de manzanillo', na=False),
    df['Municipio_Base'].str.contains(r'tecom[aá]n', na=False),
    df['Municipio_Base'].str.contains(r'tonila', na=False),
    df['Municipio_Base'].str.contains(r'aquila', na=False),
    df['Municipio_Base'].str.contains(r'coahuayana', na=False),
    df['Municipio_Base'].str.contains(r'coquimatl[aá]n|coquimatlan', na=False)
]

# 3️⃣ Resultado
resultados = [
    'Colima',
    'Villa de Álvarez',
    'Cuauhtémoc',
    'Comala',
    'Manzanillo',
    'Tecomán',
    'Tonila',
    'Aquila',
    'Coahuayana',
    'Coquimatlán'
]

# 4️⃣ Nueva columna
df['Municipio_Normalizado'] = np.select(condiciones, resultados, default='Otro')

# ========================================
# 📌 VISTA RESUMIDA
# ========================================
st.subheader("🏠 Clasificación de Municipios (Agrupados)")
st.dataframe(df[['Municipio donde vive actualmente', 'Municipio_Normalizado']].drop_duplicates().sort_values('Municipio_Normalizado'))

# ========================================
# 🔢 Conteo
# ========================================
st.subheader("📊 Conteo por Municipio Normalizado")
conteo = df['Municipio_Normalizado'].value_counts().reset_index()
conteo.columns = ['Municipio_Normalizado', 'Cantidad']
st.dataframe(conteo)

# ========================================
# 🥧 Gráfica opcional
# ========================================
st.subheader("🥧 Distribución Gráfica (Municipios Normalizados)")

fig = conteo.plot.pie(y='Cantidad', labels=conteo['Municipio_Normalizado'], autopct='%1.1f%%', legend=False, figsize=(6, 6)).get_figure()
st.pyplot(fig)
