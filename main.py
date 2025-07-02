import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========================================
# 🔗 CONFIGURACIÓN GENERAL
# ========================================
st.set_page_config(layout="wide")

st.title("📊 Reporte Demográfico y de Oportunidades de Mejora")
st.markdown("""
**Instituto Tecnológico de Colima 2025**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ========================================
# 🔗 CARGA DE DATOS DESDE GOOGLE SHEETS
# ========================================
url_csv = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url_csv)

st.success(f"✅ Datos cargados correctamente ({len(df)} registros).")
st.dataframe(df.head())

# ========================================
# 🧹 NORMALIZAR MUNICIPIOS
# ========================================
df['Municipio_Base'] = df['Municipio donde vive actualmente'].str.lower().str.strip()

condiciones = [
    df['Municipio_Base'].str.contains(r'\bcolima\b|colima colima|colima\.colima|colima, colima|colima,col|colima\. col', na=False),
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

df['Municipio_Normalizado'] = np.select(condiciones, resultados, default='Otro')

# ========================================
# ✅ CONTEO NORMALIZADO
# ========================================
st.subheader("📌 Municipios Normalizados")
st.dataframe(df[['Municipio donde vive actualmente', 'Municipio_Normalizado']].drop_duplicates().sort_values('Municipio_Normalizado'))

conteo_mun = df['Municipio_Normalizado'].value_counts().reset_index()
conteo_mun.columns = ['Municipio_Normalizado', 'Cantidad']

st.subheader("📊 Conteo de Municipios")
st.dataframe(conteo_mun)

fig1, ax1 = plt.subplots(figsize=(6, 6))
ax1.pie(conteo_mun['Cantidad'], labels=conteo_mun['Municipio_Normalizado'], autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# ========================================
# ⚡ NORMALIZAR INSTITUCIÓN (EJEMPLO)
# ========================================
df['Institucion_Base'] = df['¿De qué institución académica egresaste?'].str.lower().str.strip()

cond_institucion = [
    df['Institucion_Base'].str.contains(r'colima', na=False),
    df['Institucion_Base'].str.contains(r'ateneo', na=False),
    df['Institucion_Base'].str.contains(r'isenco', na=False),
    df['Institucion_Base'].str.contains(r'icep', na=False),
    df['Institucion_Base'].str.contains(r'ctys|cbtis|cetis|bachillerato profesionalizante', na=False),
    df['Institucion_Base'].str.contains(r'universidad privada|tec|univa|martí|jose marti', na=False)
]

res_institucion = [
    'Universidad de Colima',
    'Ateneo',
    'ISENCO',
    'ICEP',
    'Bachillerato Profesionalizante',
    'Universidad Privada'
]

df['Institucion_Normalizada'] = np.select(cond_institucion, res_institucion, default='Otro')

st.subheader("🏫 Instituciones Normalizadas")
st.dataframe(df[['¿De qué institución académica egresaste?', 'Institucion_Normalizada']].drop_duplicates().sort_values('Institucion_Normalizada'))

conteo_inst = df['Institucion_Normalizada'].value_counts().reset_index()
conteo_inst.columns = ['Institucion_Normalizada', 'Cantidad']

fig2, ax2 = plt.subplots(figsize=(6, 6))
ax2.pie(conteo_inst['Cantidad'], labels=conteo_inst['Institucion_Normalizada'], autopct='%1.1f%%', startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

# ========================================
# 📊 OTRAS VARIABLES CATEGÓRICAS
# ========================================
columnas_categoricas = [
    "Seleccione su sexo",
    "¿A qué carrera desea ingresar?",
    "¿Quién lo ha apoyado económicamente en sus estudios previos?",
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "En el último año, ¿ha acudido a consulta por atención psicológica?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?"
]

for col in columnas_categoricas:
    if col not in df.columns:
        continue

    st.subheader(f"🥧 Distribución: {col}")

    conteo = df[col].value_counts().reset_index()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(conteo[col], labels=conteo['index'], autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ========================================
# 📌 VARIABLES CONTINUAS Y ATÍPICOS
# ========================================
def convertir_rango_general(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "ninguna" in valor:
        return 0
    if "menos de" in valor:
        num = [float(s) for s in valor.split() if s.replace('.', '', 1).isdigit()]
        return num[0] / 2 if num else np.nan
    if "a" in valor:
        partes = valor.split("a")
        try:
            minimo = float(partes[0].strip())
            maximo = float(partes[1].split()[0].strip())
            return (minimo + maximo) / 2
        except:
            return np.nan
    try:
        return float(valor)
    except:
        return np.nan

# Aplica conversión ejemplo
if "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?" in df.columns:
    df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango_general)

col_continuas = ["Triste_Num"]
for col in col_continuas:
    if col not in df.columns:
        continue

    st.subheader(f"🧩 Análisis de atípicos: {col}")
    data = df[[col]].dropna()
    Q1 = data[col].quantile(0.25)
    Q3 = data[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]
    if not outliers.empty:
        st.warning(f"⚠️ {len(outliers)} dato(s) atípico(s) encontrados en '{col}':")
        st.dataframe(outliers)
    else:
        st.success(f"✅ No se encontraron datos atípicos en '{col}'.")

st.markdown("**Fin del reporte.**")
