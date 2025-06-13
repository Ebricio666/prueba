import streamlit as st
import pandas as pd

# requirements.txt
# streamlit
# pandas

st.title("Cuestionario de Habilidades para el Trabajo en Equipo")

st.markdown("""
Seleccione el nivel con el que se identifica en cada una de las siguientes afirmaciones:
- 1 = Nada de acuerdo
- 2 = Poco de acuerdo
- 3 = Medianamente de acuerdo
- 4 = De acuerdo
- 5 = Totalmente de acuerdo
""")

preguntas = [
    "Colaboro de forma activa para que los acuerdos se cumplan.",
    "Escucho y valoro las ideas de los demás integrantes del equipo.",
    "Prefiero trabajar solo que colaborar con otros.",
    "Me siento capaz de coordinar un equipo hacia metas comunes.",
    "Promuevo la participación equitativa de todos los miembros del equipo.",
    "Tomo decisiones considerando tanto la lógica como el bienestar del grupo.",
    "Me adapto fácilmente a cambios en la planeación o ejecución del trabajo.",
    "Puedo cambiar mi enfoque si las condiciones del entorno lo requieren.",
    "Me cuesta adaptarme cuando hay cambios imprevistos.",
    "Me aseguro de que mis mensajes sean claros y comprensibles.",
    "Escucho activamente antes de emitir una opinión.",
    "Doy retroalimentación constructiva y con respeto.",
    "Analizo diferentes alternativas antes de decidir cómo actuar.",
    "Tomo decisiones fundamentadas en datos y evidencia.",
    "Evito enfrentar problemas difíciles directamente.",
    "Busco mejorar mis resultados sin afectar el trabajo de otros.",
    "Me esfuerzo por destacar con base en la calidad de mi trabajo.",
    "Comparto mis logros y aprendizajes para motivar a mis colegas."
]

respuestas = {}

for i, pregunta in enumerate(preguntas):
    respuestas[pregunta] = st.slider(
        label=f"{i+1}. {pregunta}",
        min_value=1,
        max_value=5,
        value=3,
        format="%d"
    )

if st.button("Enviar respuestas"):
    df_respuestas = pd.DataFrame(respuestas, index=[0])
    st.write("### Resumen de tus respuestas:")
    st.dataframe(df_respuestas.T.rename(columns={0: "Puntaje"}))

    csv = df_respuestas.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Descargar respuestas en CSV",
        data=csv,
        file_name='respuestas_cuestionario.csv',
        mime='text/csv'
    )

