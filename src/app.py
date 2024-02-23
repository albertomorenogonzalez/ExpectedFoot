import streamlit as st
import os
import numpy as np
from googletrans import Translator
import joblib
user_image_route = os.path.join("media","usuario.png")
modelo_ruta = 'model/xg_model_decision_tree_regressor.pkl'
xg_model_decision_tree_regressor = joblib.load(modelo_ruta)


ruta_imagen_local = os.path.join("media", "logo.png")
ruta_imagen_local_pelota = os.path.join("media", "logo_pelota.png")
st.set_page_config(page_icon=ruta_imagen_local_pelota, page_title="ExpectedFoot")


page = """
<style>
[data-testid=stAppViewContainer]{
    background-color: #169E79
}
.sidebar{
    background-color: #244155; 
}
.css-1ytj5ow {
    background-color: #244155; /* Puede que necesites ajustar esto */
}
</style>
"""

st.markdown(page, unsafe_allow_html=True)


def contiene_solo_letras(cadena):
    return all(caracter.isalpha() or caracter.isspace() for caracter in cadena)
if "jugador" not in st.session_state:
    st.session_state["jugador"]=""
if "games" not in st.session_state:
    st.session_state["games"]=0
if "goals" not in st.session_state:
    st.session_state["goals"]=0
if "assists" not in st.session_state:
    st.session_state["assists"]=0
if "pens_att" not in st.session_state:
    st.session_state["pens_att"]=0
if "progressive_carries" not in st.session_state:
    st.session_state["progressive_carries"]=0
if "pens_made" not in st.session_state:
    st.session_state["pens_made"]=0
correct_responses = [
    "Introduce el nombre del jugador que desea analizar",
  f"¿Cuántos partidos ha jugado? ",
 f"¿Cuántos goles ha marcado?",
 f"¿Cuántas asistencias ha realizado? ",
  f"¿Cuántos penaltis ha ejecutado? ",
   f"¿Cuántos goles de penalti ha marcado de los "+str(st.session_state["pens_att"])+" penaltis ejecutados?",
   f"¿Cuántos avances con la pelota hacia el área ha realizado el jugador con éxito? ",
  "Analizando datos..."
]
error_responses = [
   "Por favor, introduce correctamente el nombre del jugador.",
   f"el jugador no ha jugado ningún partido. No podemos seguir analizando a este jugador.", 
   "Error: introduzca un número natural",
   "Error: La cantidad de goles de penalti no puede ser mayor que la cantidad total de goles marcados o penaltis ejecutados.",
   ]
pasos=["nombre_jugador","partidos_jugados","goles_marcados","asistencias_realizadas","penaltis_ejecutados","goles_penaltis","avances_exito","analizando_datos"]
if "paso" not in st.session_state:
    st.session_state["paso"]=pasos[0]
def response(user_input):
   jugador=st.session_state["jugador"]
   games=st.session_state["games"]
   goals=st.session_state["goals"]
   assists=st.session_state["assists"]
   pens_att=st.session_state["pens_att"]
   pens_made=st.session_state["pens_made"]
   progressive_carries=st.session_state["progressive_carries"]
   # "Introduce el nombre del jugador que desea analizar",
   if st.session_state["paso"]==pasos[0]:
      if contiene_solo_letras(user_input):
         st.session_state["paso"]=pasos[1]
         st.session_state["jugador"]=user_input
         return f"¿Cuántos partidos ha jugado el jugador? "
      else:
         return error_responses[0]
    #  f"¿Cuántos partidos ha jugado? ",
   if st.session_state["paso"]==pasos[1]:
      if not user_input.isdigit():
         return error_responses[2]
      elif user_input==0:
         st.session_state["paso"]=pasos[0]
         return error_responses[1]
      else:
         st.session_state["paso"]=pasos[2]
         st.session_state["games"]=user_input
         return  f"¿Cuántos goles ha marcado el jugador?"
    # f"¿Cuántos goles ha marcado?",
   if st.session_state["paso"] == pasos[2]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            st.session_state["paso"] = pasos[3]
            st.session_state["goals"] = int(user_input)
            return f"¿Cuántas asistencias ha realizado el jugador? "
    # f"¿Cuántas asistencias ha realizado? ",
   if st.session_state["paso"] == pasos[3]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            st.session_state["paso"] = pasos[4]
            st.session_state["assists"] = int(user_input)
            return f"¿Cuántos penaltis ha ejecutado el jugador? "
    # f"¿Cuántos penaltis ha ejecutado? ",
   if st.session_state["paso"] == pasos[4]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            st.session_state["paso"] = pasos[5]
            st.session_state["pens_att"]= int(user_input)
            return f"¿Cuántos goles de penalti ha marcado el jugador de los "+str(st.session_state["pens_att"])+" penaltis ejecutados?"
    # f"¿Cuántos goles de penalti ha marcado el de los penaltis ejecutados? ",
   if st.session_state["paso"] == pasos[5]:
        if not user_input.isdigit():
            return error_responses[2]
        elif int(user_input) > st.session_state["goals"] or int(user_input) > st.session_state["pens_att"]:
            return error_responses[3]
        else:
            st.session_state["paso"] = pasos[6]
            st.session_state["pens_made"] = int(user_input)
            return correct_responses[6]
    # "¿Cuántos avances con la pelota hacia el área ha realizado con éxito? ",
   if st.session_state["paso"] == pasos[6]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            st.session_state["paso"] = pasos[7]
            st.session_state["progressive_carries"] = int(user_input)
            return correct_responses[7]
    # "Analizando datos..."
  
    
def compile_stats(games, goals, assists, pens_att, pens_made, progressive_carries):  
    goals_assists=goals+assists
    goals_pens = goals - pens_made
    new_data = [[games, goals, assists, goals_assists, pens_att, pens_made, goals_pens, progressive_carries]]
    prediction = xg_model_decision_tree_regressor.predict(new_data)
    if st.session_state["pens_made"] == 0:
        return  (f"> el jugador ha marcado {goals} goles en {games} partidos, asistiendo {assists} veces, ha ejecutado {pens_att} penaltis, de los cuales no marcado ninguno y los goles marcados en jugada han sido {goals_pens}.\n **El resultado de los goles esperados del jugador es de {prediction[0]:.2f} goles por temporada.**")
    else:
        return (f"> el jugador ha marcado {goals} goles en {games} partidos, asistiendo {assists} veces, ha ejecutado {pens_att} penaltis, de los cuales ha marcado {pens_made} y los goles marcados en jugada han sido {goals_pens}.\n **El resultado de los goles esperados del jugador es de {prediction[0]:.2f} goles por temporada.**")


translator = Translator()
if "language" not in st.session_state:
    st.session_state["language"] = ""

translator = Translator()
if "language" not in st.session_state:
    st.session_state["language"] = ""
def translate(text):
    
    if text != st.session_state["jugador"] and text is not None and not text.isdigit() and text!="":
        try:
            translated_text = ""
            if st.session_state["language"]=="":
                return text

            if st.session_state["jugador"]!="":
                text=text.replace(" "+st.session_state["jugador"]+" "," x")

            if st.session_state["language"] == "español":
                translation = translator.translate(text, dest='es')
            elif  st.session_state["language"] == "inglés":
                translation = translator.translate(text, dest='en')
            elif  st.session_state["language"] == "francés":
                translation = translator.translate(text, dest='fr')
            elif  st.session_state["language"] == "italiano":
                translation = translator.translate(text, dest='it')
            elif  st.session_state["language"] == "alemán":
                translation = translator.translate(text, dest='de')

            translated_text = translation.text
            translated_text = translated_text.replace("Pie esperado", "ExpectedFoot")
            translated_text = translated_text.replace("ExpectaDfoot", "ExpectedFoot")
            translated_text = translated_text.replace("AwayAdfoot", "ExpectedFoot")
            translated_text = translated_text.replace("aspettativa", "ExpectedFoot")
            translated_text = translated_text.replace("Erwartungs", "ExpectedFoot-")

            if st.session_state["jugador"]!="":
                translated_text = translated_text.replace(" x", " "+st.session_state["jugador"])
            if translated_text is None or translated_text=="":
                return text
            return translated_text
        except Exception as e:
            print(f"Error en la traducción: {e}")
    else:
        return text
col1, col2, col3 = st.columns([1, 3, 1])
# Espacio en blanco para las columnas izquierda y derecha
with col1:
    st.write("")
with col3:
    st.write("")
# Colocar la imagen en la columna central
with col2:
    st.image(ruta_imagen_local, width=200, use_column_width=True)



colu1, colu2, colu3, colu4, colu5 = st.columns([1, 1, 1, 1, 1])

select_language_msg = translate("Selecciona el idioma: ")
spanish_option = "Español"
english_option = "English"
french_option="Français"
italian_option="Italiano"
german_option="Deutsch"

    
with colu1:
    container_es = st.container()
    if container_es.button(spanish_option, key="A"):
        st.session_state["language"] = "español"
with colu2:
    container_en = st.container()
    if container_en.button(english_option,key="B"):
        st.session_state["language"] = "inglés"
with colu3:
    container_en = st.container()
    if container_en.button(french_option,key="C"):
        st.session_state["language"] = "francés"
with colu4:
    container_en = st.container()
    if container_en.button(italian_option,key="D"):
        st.session_state["language"] = "italiano"
with colu5:
    container_en = st.container()
    if container_en.button(german_option,key="E"):
        st.session_state["language"] = "alemán"


if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role":"assistant","avatar":"⚽" ,"content":translate("¡Hola! Soy el asistente de ExpectedFoot, tu analizador de jugadores.")}]
  st.session_state["messages"].append({"role":"assistant", "avatar":"⚽","content":translate(correct_responses[0])})
if "messages" in st.session_state:
   for msg in st.session_state["messages"]:
    st.chat_message(msg["role"],avatar=msg["avatar"]).write(translate(msg["content"]))
   if user_input := st.chat_input():
     if st.session_state["messages"][-1]["role"] != "user":
        st.session_state["messages"].append({"role": "user","avatar":user_image_route,"content": user_input})
        st.chat_message("user",avatar="🦖").write(user_input)
        responseMessage = translate(response(user_input))
        st.session_state["messages"].append({"role": "assistant","avatar":"⚽", "content": responseMessage})
        st.chat_message("assistant",avatar="⚽").write(responseMessage)
        if responseMessage==correct_responses[7]:
            newPrediction=compile_stats( st.session_state["games"],
                                        st.session_state["goals"],
                                        st.session_state["assists"],
                                        st.session_state["pens_att"], 
                                        st.session_state["pens_made"], 
                                        st.session_state["progressive_carries"])
            st.session_state["paso"]=pasos[0]
            st.session_state["messages"].append({"role": "assistant","avatar":"⚽" , "content":translate(newPrediction)})
            st.chat_message("assistant",avatar="⚽").write(translate(newPrediction))
            st.session_state["messages"].append({"role":"assistant", "avatar":"⚽" ,"content":translate("Si quiere analizar otro jugador introduzca su nombre")})
            st.chat_message("assistant",avatar="⚽").write(translate("Si quiere analizar otro jugador introduzca su nombre"))
