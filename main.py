import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Análisis de Datos por Docente")

# 1. Subir archivo desde el escritorio
uploaded_file = st.file_uploader("Carga el archivo Excel con los datos de estudiantes", type=[".xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # 2. Solicitar homoclave del docente
    homoclave = st.text_input("Introduce la homoclave del docente (ej. PROF1003):").strip().upper()

    if homoclave:
        df_docente = df[df['Homoclave del docente'].str.upper() == homoclave]

        if df_docente.empty:
            st.warning("No se encontraron datos para esa homoclave.")
        else:
            st.success(f"Datos filtrados para el docente con homoclave: {homoclave}")
            st.dataframe(df_docente)

            # 4. Agrupar por 'Bachillerato'
            st.subheader("Distribución por Bachillerato")
            bachillerato_group = df_docente['Bachillerato'].value_counts().reset_index()
            bachillerato_group.columns = ['Bachillerato', 'Cantidad']
            st.dataframe(bachillerato_group)

            # 5. Promedio Bachillerato por rangos
            st.subheader("Distribución por rangos de Promedio de Bachillerato")
            bins = [6.9, 7.9, 8.9, 9.9, 10.1]
            labels = ['7.0 - 7.9', '8.0 - 8.9', '9.0 - 9.9', '10.0']
            df_docente['Rango Promedio'] = pd.cut(df_docente['Promedio Bachillerato'], bins=bins, labels=labels, right=True)
            promedio_group = df_docente['Rango Promedio'].value_counts().sort_index().reset_index()
            promedio_group.columns = ['Rango de Promedio', 'Cantidad']
            st.dataframe(promedio_group)

            # 6. Agrupar por Alergias
            st.subheader("Distribución por tipo de Alergias")
            alergias_group = df_docente['Alergias'].value_counts(dropna=False).reset_index()
            alergias_group.columns = ['Alergias', 'Cantidad']
            st.dataframe(alergias_group)

            # 7. Agrupar por Padecimientos
            st.subheader("Distribución por tipo de Padecimientos")
            padecimientos_group = df_docente['Padecimientos'].value_counts(dropna=False).reset_index()
            padecimientos_group.columns = ['Padecimientos', 'Cantidad']
            st.dataframe(padecimientos_group)

            # 8. Variables categóricas adicionales
            columnas_extra = [
                'Sexo', '¿Actualmente trabaja?', 'Lugar donde vive', '¿Vive con?', 'Grupo sanguíneo',
                '¿Cuenta con un lugar adecuado para estudiar en casa?',
                '¿Tiene acceso constante a internet y computadora?',
                '¿Se ha sentido triste o desmotivado frecuentemente en las últimas dos semanas?',
                '¿A quién acudiría si tuviera un problema emocional o académico?',
                '¿Ha recibido atención psicológica en el último año?',
                '¿Quién lo(a) apoya económicamente durante sus estudios?',
                '¿Cuenta con personas cercanas que lo(a) motivan a continuar con su carrera?'
            ]

            for col in columnas_extra:
                if col in df_docente.columns:
                    st.subheader(f"Distribución por {col}")
                    grupo = df_docente[col].value_counts(dropna=False).reset_index()
                    grupo.columns = [col, 'Cantidad']
                    st.dataframe(grupo)

    # 9. Boxplots y detección de datos atípicos
    st.header("Boxplots y valores atípicos")
    columnas_numericas = [
        'Promedio Bachillerato',
        'Edad',
        '¿Cuál fue su promedio final en el último ciclo escolar?'
    ]
    for col in columnas_numericas:
        if col in df.columns:
            st.subheader(f"Análisis para: {col}")
            fig, ax = plt.subplots()
            ax.boxplot(df[col].dropna(), vert=False)
            ax.set_title(f'Boxplot de: {col}')
            ax.set_xlabel(col)
            st.pyplot(fig)

            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - 1.5 * IQR
            upper = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower) | (df[col] > upper)]

            if not outliers.empty:
                st.warning(f"Se encontraron {len(outliers)} dato(s) atípico(s) en {col}:")
                columnas_a_mostrar = ['Nombre', col] if 'Nombre' in df.columns else [col]
                st.dataframe(outliers[columnas_a_mostrar])
            else:
                st.info(f"No se encontraron datos atípicos en {col}.")

    # 10. Barras apiladas normalizadas
    st.header("Barras Apiladas Normalizadas")
    columnas_categoricas = [
        '¿Actualmente trabaja?',
        'Lugar donde vive',
        'Bachillerato',
        '¿A quién acudiría si tuviera un problema emocional o académico?',
        '¿Quién lo(a) apoya económicamente durante sus estudios?'
    ]

    for columna in columnas_categoricas:
        if columna in df.columns:
            conteo = df[columna].value_counts(dropna=False)
            porcentaje = (conteo / conteo.sum()) * 100
            categorias = porcentaje.index.tolist()

            fig, ax = plt.subplots(figsize=(10, 2))
            left = 0
            for cat in categorias:
                val = porcentaje[cat]
                ax.barh(0, val, left=left, label=str(cat))
                left += val

            ax.set_xlim(0, 100)
            ax.set_xlabel('Porcentaje (%)')
            ax.set_yticks([])
            ax.set_title(f'Distribución: {columna}')
            ax.legend(title='Respuesta', bbox_to_anchor=(1.05, 1), loc='upper left')
            st.pyplot(fig)
