import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

st.markdown("""
# Reporte gráfico de datos demográficos y áreas de oportunidad de los aspirantes al ingreso a las diversas carreras del Instituto Tecnológico de Colima 2025  
**Elaborado por:** Dra. Elena Elsa Bricio-Barrios, Dr. Santiago Arceo-Díaz y Psicóloga Martha Cecilia Ramírez-Guzmán
""")

# ==========================
# SUBIR ARCHIVO
# ==========================
uploaded_file = st.file_uploader("📁 Sube el archivo Excel con los datos", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ==========================
    # VALIDAR ENCABEZADOS
    # ==========================
    headers = df.columns.tolist()
    st.subheader("📌 Encabezados detectados:")
    st.write(headers)

    duplicados = df.columns[df.columns.duplicated()].unique().tolist()
    if duplicados:
        st.warning("⚠️ Encabezados duplicados encontrados:")
        for col in duplicados:
            st.write(f"- {col}")
    else:
        st.success("✅ No hay encabezados duplicados.")

    encabezados_esperados = [
        "Fecha",
        "Homoclave del docente",
        "Correo",
        "Carrera",
        "Nombre",
        "Sexo",
        "Edad",
        "Lugar donde vive",
        "¿Vive con?",
        "Tiempo de desplazamiento",
        "Trabaja",
        "Bachillerato",
        "Promedio",
        "Tel de contacto",
        "Alergia",
        "Enfermedades",
        "Grupo sanguíneo",
        "Espacio para trabajar",
        "Acceso a internet y pc",
        "Tiempo estudio",
        "Tiempo",
        "Triste",
        "Psicologo",
        "Apoyo carrera"
    ]

    faltantes = [col for col in encabezados_esperados if col not in headers]
    if faltantes:
        st.error("❌ Encabezados faltantes:")
        for col in faltantes:
            st.write(f"- {col}")
        st.stop()
    else:
        st.success("✅ Todos los encabezados esperados están presentes.")

    st.subheader("📊 Todos los datos cargados")
    st.dataframe(df)

    # ==========================
    # FUNCIONES PARA CONVERTIR RANGOS
    # ==========================
    def convertir_rango_promedio(valor):
        if pd.isna(valor):
            return np.nan
        if isinstance(valor, (int, float)):
            return valor
        if isinstance(valor, str) and "a" in valor:
            partes = valor.split("a")
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

    def convertir_rango_tiempo_desplazamiento(valor):
        if pd.isna(valor):
            return np.nan
        valor = str(valor).lower()
        if "menos de" in valor:
            try:
                num = [int(s) for s in valor.split() if s.isdigit()][0]
                return num / 2
            except:
                return np.nan
        elif "de" in valor and "a" in valor:
            partes = valor.replace("min", "").split("a")
            try:
                minimo = int(partes[0].split()[-1].strip())
                maximo = int(partes[1].strip())
                return (minimo + maximo) / 2
            except:
                return np.nan
        else:
            return np.nan

    def convertir_rango_general(valor):
        if pd.isna(valor):
            return np.nan
        valor = str(valor).lower()
        if "ninguna" in valor:
            return 0
        if "menos de" in valor:
            try:
                num = [float(s) for s in valor.split() if s.replace('.', '', 1).isdigit()][0]
                return num / 2
            except:
                return np.nan
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

    # ==========================
    # APLICAR CONVERSIONES
    # ==========================
    if "Promedio" in df.columns:
        df["Promedio_Num"] = df["Promedio"].apply(convertir_rango_promedio)

    if "Tiempo de desplazamiento" in df.columns:
        df["Tiempo_desplazamiento_Num"] = df["Tiempo de desplazamiento"].apply(convertir_rango_tiempo_desplazamiento)

    if "Tiempo" in df.columns:
        df["Tiempo_Num"] = df["Tiempo"].apply(convertir_rango_general)

    if "Triste" in df.columns:
        df["Triste_Num"] = df["Triste"].apply(convertir_rango_general)

    # ==========================
    # BÚSQUEDA OPCIONAL
    # ==========================
    nombre_cols = [col for col in df.columns if "Nombre" in col]
    nombre_col = nombre_cols[0] if nombre_cols else None

    if nombre_col:
        if st.radio("🔍 ¿Desea realizar una búsqueda personalizada?", ["No", "Sí"]) == "Sí":
            nombre_estudiante = st.text_input(f"Introduce el nombre del estudiante (columna '{nombre_col}')").strip()
            if nombre_estudiante:
                df_estudiante = df[
                    df[nombre_col].astype(str).str.lower().str.contains(nombre_estudiante.lower(), na=False)
                ]
                if df_estudiante.empty:
                    st.warning("⚠️ No se encontró al estudiante.")
                else:
                    st.subheader(f"🎓 Datos del estudiante: {nombre_estudiante}")
                    st.dataframe(df_estudiante)

    # ==========================
    # VARIABLES CATEGÓRICAS
    # ==========================
    columnas_categoricas = [
        "Sexo",
        "Edad",
        "Carrera",
        "Lugar donde vive",
        "¿Vive con?",
        "Tiempo de desplazamiento",
        "Trabaja",
        "Bachillerato",
        "Promedio",
        "Tiempo",
        "Triste",
        "Espacio para trabajar",
        "Acceso a internet y pc",
        "Psicologo",
        "Apoyo carrera"
    ]

    columnas_categoricas = list(dict.fromkeys(columnas_categoricas))

    for col in columnas_categoricas:
        if col not in df.columns:
            continue

        st.markdown(f"### 📊 Distribución: {col}")

        conteo = df[col].value_counts(dropna=False).sort_index()
        porcentaje = (conteo / conteo.sum()) * 100

        fig, ax = plt.subplots(figsize=(10, 2))
        left = 0
        for cat in porcentaje.index:
            val = porcentaje[cat]
            n = conteo[cat]
            label = f"{cat} ({n})"
            ax.barh(0, val, left=left, label=label)
            left += val

        ax.set_xlim(0, 100)
        ax.set_xlabel('Porcentaje (%)')
        ax.set_yticks([])
        ax.legend(title='Respuesta', bbox_to_anchor=(1.02, 1), loc='upper left')
        st.pyplot(fig)

    # ==========================
    # VARIABLES CONTINUAS CON BOXPLOTS
    # ==========================
    columnas_continuas = [
        "Edad",
        "Promedio_Num",
        "Tiempo estudio",
        "Tiempo_desplazamiento_Num",
        "Tiempo_Num",
        "Triste_Num"
    ]

    for col in columnas_continuas:
        if col not in df.columns:
            continue

        df[col] = pd.to_numeric(df[col], errors='coerce')
        datos = df[[col]].dropna()

        if datos.empty:
            continue

        Q1 = datos[col].quantile(0.25)
        Q3 = datos[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        # Histograma por rangos
        if "Edad" in col:
            bins = np.arange(17, 22, 2)
        elif "Promedio" in col:
            bins = np.arange(6.0, 10.5, 0.5)
        elif "Tiempo estudio" in col:
            bins = 10
        elif "Tiempo_desplazamiento" in col:
            bins = np.arange(0, 70, 10)
        elif "Tiempo_Num" in col:
            bins = np.arange(0, 5, 1)
        elif "Triste_Num" in col:
            bins = np.arange(0, 12, 2)
        else:
            bins = 10

        df.loc[:, 'Rango_' + col] = pd.cut(df[col], bins=bins)
        conteo_barras = df['Rango_' + col].value_counts().sort_index()

        st.markdown(f"### 📈 Histograma: {col}")
        fig, ax = plt.subplots(figsize=(8, 4))
        conteo_barras.plot(kind='bar', ax=ax, color='skyblue')
        ax.set_ylabel('Número de estudiantes')
        ax.set_xlabel('Rangos')
        ax.grid(axis='y')
        st.pyplot(fig)

        st.markdown(f"### 📊 Boxplot: {col}")
        fig2, ax2 = plt.subplots(figsize=(6, 4))
        ax2.boxplot(datos[col], vert=False)
        ax2.set_xlabel(col)
        ax2.set_title(f"Boxplot: {col}")
        st.pyplot(fig2)

        outliers = datos[(datos[col] < lower) | (datos[col] > upper)]
        if not outliers.empty:
            st.warning(f"⚠️ Se encontraron {len(outliers)} dato(s) atípico(s) en '{col}':")
            st.dataframe(outliers)
        else:
            st.success(f"✅ No se encontraron datos atípicos en '{col}'.")
