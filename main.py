# ============================================
# ✅ app.py
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
# 📊 Reporte gráfico de datos demográficos y áreas de oportunidad  
**Instituto Tecnológico de Colima 2025**  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ============================================
# 📌 VINCULAR DATOS GOOGLE SHEETS COMO CSV
# ============================================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)

st.success("✅ Datos cargados correctamente desde Google Sheets.")
st.subheader("📑 Vista previa de los datos")
st.dataframe(df)

# ============================================
# 📌 AGRUPACIÓN PERSONALIZADA
# ============================================

# Municipio agrupado
def agrupar_municipio(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip().lower()
    if "villa" in x:
        return "Villa de Álvarez"
    elif "colima" in x:
        return "Colima"
    elif "coquimatlan" in x:
        return "Coquimatlán"
    elif "manzanillo" in x:
        return "Manzanillo"
    elif "cuauhtemoc" in x:
        return "Cuauhtémoc"
    elif "tecoman" in x:
        return "Tecomán"
    elif "comala" in x:
        return "Comala"
    elif "armeria" in x:
        return "Armería"
    elif "aquila" in x:
        return "Aquila"
    elif "tonila" in x:
        return "Tonila"
    elif "ixtlahuacan" in x:
        return "Ixtlahuacán"
    else:
        return "Otros"

df["Municipio Agrupado"] = df["Municipio donde vive actualmente"].apply(agrupar_municipio)

# Institución agrupada
def agrupar_escuela(x):
    if pd.isna(x):
        return np.nan
    x = str(x).strip().lower()
    if "universidad de colima" in x:
        return "Bachillerato UdeC"
    elif "cetis" in x or "cbtis" in x or "cecyte" in x or "cbta" in x or "emsad" in x or "conalep" in x:
        return "Bachillerato profesionalizante"
    elif "isenco" in x:
        return "ISENCO"
    elif "privada" in x or "univa" in x or "anahuac" in x or "tec de monterrey" in x or "vizcaya" in x or "univer" in x:
        return "Universidad Privada"
    else:
        return "Otros"

df["Escuela Agrupada"] = df["¿De qué institución académica egresaste?"].apply(agrupar_escuela)

# ============================================
# 📌 CONVERSIÓN DE VARIABLES NUMÉRICAS
# ============================================

def convertir_promedio(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).strip().replace(",", ".")
    if "a" in valor:
        partes = valor.split("a")
        try:
            minimo = float(partes[0])
            maximo = float(partes[1])
            return (minimo + maximo) / 2
        except:
            return np.nan
    try:
        return float(valor)
    except:
        return np.nan

df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_promedio)

# ============================================
# 📊 GRÁFICAS DE PASTEL COMPLETAS
# ============================================

columnas_categoricas = [
    "Seleccione su sexo",
    "¿A qué carrera desea ingresar?",
    "En este momento, usted",
    "¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?",
    "Actualmente, ¿realiza trabajo remunerado?",
    "¿Quién lo ha apoyado económicamente en sus estudios previos?",
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?",
    "En el último año, ¿ha acudido a consulta por atención psicológica?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?",
    "Municipio Agrupado",
    "Escuela Agrupada"
]

for col in columnas_categoricas:
    if col not in df.columns:
        continue

    st.markdown(f"### 🥧 Distribución: {col}")
    conteo = df[col].value_counts(dropna=False).sort_index()
    porcentaje = (conteo / conteo.sum()) * 100

    etiquetas = [f"{k} ({v})" for k, v in zip(conteo.index, conteo.values)]
    sizes = porcentaje.values

    fig, ax = plt.subplots(figsize=(5, 5))
    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
    )
    ax.axis('equal')
    ax.set_title(f"Distribución: {col}")
    ax.legend(wedges, etiquetas, title="Categorías", bbox_to_anchor=(1, 0.5), loc="center left")
    st.pyplot(fig)

# ============================================
# 📊 DETECCIÓN DE DATOS ATÍPICOS
# ============================================

columnas_continuas = ["Promedio_Num"]

for col in columnas_continuas:
    datos = df[[col]].dropna()
    if datos.empty:
        continue

    Q1 = datos[col].quantile(0.25)
    Q3 = datos[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    st.markdown(f"## 🧩 Área de oportunidad: {col}")
    if not outliers.empty:
        st.warning(f"⚠️ Se encontraron {len(outliers)} dato(s) atípico(s) en '{col}':")
        st.dataframe(outliers)
    else:
        st.success(f"✅ No se encontraron datos atípicos en '{col}'.")
