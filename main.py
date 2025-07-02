# ============================================
# app.py - Reporte Streamlit
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================
# 📌 CONFIGURACIÓN Y TÍTULO
# ============================================

st.set_page_config(layout="wide")

st.markdown("""
# 📊 Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes 2025
**Instituto Tecnológico de Colima**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ============================================
# 📌 VÍNCULO A GOOGLE SHEETS (publicado como CSV)
# ============================================

url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)

st.success("✅ Datos cargados desde Google Sheets.")
st.subheader("📊 Vista previa de los datos")
st.dataframe(df)

# ============================================
# 📌 VALIDAR ENCABEZADOS
# ============================================

encabezados_esperados = [
    "Municipio donde vive actualmente",
    "¿De qué institución académica egresaste?",
    "Edad en años cumplidos",
    "¿Cuál fue tu promedio de calificación del tercer año de bachillerato?",
    "¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?",
    "¿Cuántas horas al día dedica a estudiar fuera del aula?",
    "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"
]

st.subheader("📌 Encabezados detectados:")
st.write(df.columns.tolist())

faltantes = [col for col in encabezados_esperados if col not in df.columns]
if faltantes:
    st.warning(f"⚠️ Encabezados faltantes: {faltantes}")
else:
    st.success("✅ Todos los encabezados esperados están presentes.")

# ============================================
# 📌 FUNCIONES DE CONVERSIÓN
# ============================================

def convertir_rango(valor):
    if pd.isna(valor):
        return np.nan
    v = str(valor).lower()
    if "más de" in v or "mas de" in v:
        return 23
    if "a" in v:
        partes = v.split("a")
        try:
            minimo = float(partes[0].strip())
            maximo = float(partes[1].strip())
            return (minimo + maximo) / 2
        except:
            return np.nan
    try:
        return float(v)
    except:
        return np.nan

# ============================================
# 📌 NORMALIZACIÓN MUNICIPIO
# ============================================

def normalizar_municipio(valor):
    v = str(valor).lower().strip()
    if "villa" in v:
        return "Villa de Álvarez"
    if "colima" in v:
        return "Colima"
    if "cuauhtemoc" in v or "cuahutemoc" in v:
        return "Cuauhtémoc"
    if "comala" in v or "zacualpan" in v or "suchitlan" in v:
        return "Comala"
    if "manzanillo" in v:
        return "Manzanillo"
    if "tecoman" in v:
        return "Tecomán"
    if "aquila" in v:
        return "Aquila"
    if "coahuayana" in v:
        return "Coahuayana"
    if "tonila" in v:
        return "Tonila"
    if "armeria" in v:
        return "Armería"
    if "minatitlan" in v:
        return "Minatitlán"
    if "tuxpan" in v:
        return "Tuxpan"
    if "trapiche" in v or "piscila" in v:
        return "Colima"
    if "la huerta" in v:
        return "La Huerta"
    if "coquimatlan" in v:
        return "Coquimatlán"
    if "queseria" in v:
        return "Quesería"
    return v.capitalize()

# ============================================
# 📌 NORMALIZACIÓN INSTITUCIÓN
# ============================================

def normalizar_institucion(valor):
    v = str(valor).lower().strip()
    if "universidad de colima" in v or "udc" in v:
        return "Universidad de Colima"
    if "ateneo" in v:
        return "Colegio Ateneo"
    if "adonai" in v:
        return "Instituto Adonai"
    if "isenco" in v:
        return "ISENCO"
    if "icep" in v:
        return "ICEP"
    if "vizcaya" in v:
        return "Vizcaya"
    if "univer" in v:
        return "Universidad Privada"
    if "tec de monterrey" in v or "univa" in v or "jose marti" in v or "privada" in v:
        return "Universidad Privada"
    if "cbtis" in v or "cetis" in v or "cobaem" in v or "emsad" in v or "cbta" in v or "telebachillerato" in v or "conalep" in v:
        return "Bachillerato Profesionalizante"
    if "fray pedro" in v:
        return "Fray Pedro de Gante"
    if "monte corona" in v:
        return "Instituto Monte Corona"
    if "anahuac" in v:
        return "Colegio Anáhuac"
    if "cedart" in v:
        return "CEDART Juan Rulfo"
    if "mojave high school" in v:
        return "Bachillerato Extranjero"
    return v.capitalize()

# ============================================
# 📌 APLICAR LIMPIEZAS
# ============================================

df["Municipio Normalizado"] = df["Municipio donde vive actualmente"].apply(normalizar_municipio)
df["Institución Normalizada"] = df["¿De qué institución académica egresaste?"].apply(normalizar_institucion)

# ============================================
# 📊 PASTEL AGRUPADOS
# ============================================

for col in ["Municipio Normalizado", "Institución Normalizada"]:
    st.subheader(f"Distribución: {col}")
    conteo = df[col].value_counts()
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.pie(conteo, labels=conteo.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# ============================================
# 📊 DETECCIÓN DE ATÍPICOS (Ejemplo Promedio)
# ============================================

df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango)

col = "Promedio_Num"
Q1 = df[col].quantile(0.25)
Q3 = df[col].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR
outliers = df[(df[col] < lower) | (df[col] > upper)]

st.subheader(f"Datos atípicos en {col}")
if not outliers.empty:
    st.warning(outliers)
else:
    st.success("✅ No hay datos atípicos detectados.")
