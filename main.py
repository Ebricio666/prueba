# ============================================
# 📌 IMPORTS
# ============================================
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

# ============================================
# 📌 CONFIGURACIÓN
# ============================================
st.set_page_config(layout="wide")

st.title("📊 Reporte gráfico de datos demográficos y áreas de oportunidad")
st.markdown("**Instituto Tecnológico de Colima 2025**  \n"
            "**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán")

# ============================================
# 📌 CARGAR DATOS DESDE GOOGLE SHEETS
# ============================================
url = "https://docs.google.com/spreadsheets/d/1LDJFoULKkL5CzjUokGvbFYPeZewMJBAoTGq8i-4XhNY/export?format=csv"
df = pd.read_csv(url)

st.success("✅ Datos cargados correctamente")
st.dataframe(df.head())

# ============================================
# 📌 AGRUPACIÓN MUNICIPIO
# ============================================
def agrupar_municipio(x):
    x = str(x).lower().strip()
    if "villa" in x:
        return "Villa de Álvarez"
    elif "colima" in x:
        return "Colima"
    elif "manzanillo" in x:
        return "Manzanillo"
    elif "comala" in x:
        return "Comala"
    elif "coquimatlan" in x:
        return "Coquimatlán"
    elif "cuauhtemoc" in x or "cuahutemoc" in x:
        return "Cuauhtémoc"
    elif "tecoman" in x:
        return "Tecomán"
    elif "tonila" in x:
        return "Tonila"
    elif "aquila" in x:
        return "Aquila"
    else:
        return "Otro"

df["Municipio Agrupado"] = df["Municipio donde vive actualmente"].apply(agrupar_municipio)

# ============================================
# 📌 AGRUPACIÓN BACHILLERATO
# ============================================
def agrupar_bachillerato(x):
    x = str(x).lower()
    if "universidad de colima" in x:
        return "Bachillerato U de C"
    elif "cbtis" in x or "cety" in x or "cetis" in x:
        return "Bachillerato Profesionalizante (CBTIS/CETIS)"
    elif "isenco" in x:
        return "ISENCO"
    elif "preparatoria regional" in x or "udg" in x:
        return "Preparatoria Regional UdeG"
    elif "telebachillerato" in x or "emsad" in x:
        return "Telebachillerato/EMSAD"
    elif "privada" in x or "tec de monterrey" in x or "univa" in x or "josé martí" in x:
        return "Universidad Privada"
    else:
        return "Otro"

df["Bachillerato Agrupado"] = df["¿De qué institución académica egresaste?"].apply(agrupar_bachillerato)

# ============================================
# 📌 FUNCIONES DE CONVERSIÓN DE RANGOS
# ============================================
def convertir_rango(valor):
    if pd.isna(valor):
        return np.nan
    valor = str(valor).lower()
    if "más de" in valor or "mayor" in valor:
        return 23
    if "menos de" in valor:
        return 1
    if "a" in valor:
        partes = valor.replace("min", "").split("a")
        try:
            minimo = float(partes[0].strip())
            maximo = float(partes[1].strip())
            return (minimo + maximo) / 2
        except:
            return np.nan
    try:
        return float(valor)
    except:
        return np.nan

# ============================================
# 📌 APLICAR CONVERSIONES
# ============================================
df["Edad_Num"] = df["Edad en años cumplidos"].apply(convertir_rango)
df["Desplazamiento_Num"] = df["¿Cuánto tiempo le toma desplazarse a pie o vehículo público o privado del lugar donde vive a esta Institución Académica?"].apply(convertir_rango)
df["Promedio_Num"] = df["¿Cuál fue tu promedio de calificación del tercer año de bachillerato?"].apply(convertir_rango)
df["Horas_Estudio_Num"] = df["¿Cuántas horas al día dedica a estudiar fuera del aula?"].apply(convertir_rango)
df["Triste_Num"] = df["En las últimas dos semanas ¿Cuántas veces se ha sentido desmotivado o triste?"].apply(convertir_rango)

# ============================================
# 📌 GRÁFICAS DE PASTEL
# ============================================
st.header("🥧 Diagramas de Pastel")

columnas_categoricas = [
    "Seleccione su sexo",
    "¿A qué carrera desea ingresar?",
    "Municipio Agrupado",
    "Bachillerato Agrupado",
    "Actualmente, ¿realiza trabajo remunerado?",
    "¿Cuenta con un lugar adecuado para estudiar en casa?",
    "¿Tengo acceso a internet y computadora en casa?",
    "¿Cuenta con personas que lo motivan o apoyan a continuar su carrera?"
]

for col in columnas_categoricas:
    if col in df.columns:
        conteo = df[col].value_counts()
        porcentaje = (conteo / conteo.sum()) * 100

        labels = [f"{cat} ({conteo[cat]}) - {porcentaje[cat]:.1f}%" for cat in conteo.index]

        fig, ax = plt.subplots()
        wedges, texts = ax.pie(conteo, labels=labels, startangle=90)
        ax.axis('equal')
        ax.set_title(f"Distribución: {col}")
        st.pyplot(fig)

# ============================================
# 📌 DATOS ATÍPICOS
# ============================================
st.header("📊 Detección de Datos Atípicos")

columnas_numericas = ["Edad_Num", "Desplazamiento_Num", "Promedio_Num", "Horas_Estudio_Num", "Triste_Num"]

for col in columnas_numericas:
    datos = df[col].dropna()
    Q1 = datos.quantile(0.25)
    Q3 = datos.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR

    outliers = df[(df[col] < lower) | (df[col] > upper)]

    st.subheader(f"Datos Atípicos: {col}")
    if not outliers.empty:
        st.dataframe(outliers)
    else:
        st.success(f"No se encontraron datos atípicos en {col}")

# ============================================
# 📌 EXPORTAR A PDF (opcional básico)
# ============================================
st.header("📄 Exportar PDF")

if st.button("Generar PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="📊 Reporte ITColima 2025", ln=True, align='C')

    pdf.multi_cell(0, 10, "Este reporte contiene agrupación de municipios y bachilleratos, diagramas de pastel con conteos y porcentajes, "
                          "y tablas de detección de datos atípicos.\n\nPara visualizar gráficos completos, consulte el archivo original o app online.")

    pdf.output("reporte_ITColima.pdf")
    st.success("✅ PDF generado y guardado como 'reporte_ITColima.pdf'. Descárgalo desde tu carpeta local.")
