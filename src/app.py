import streamlit as st
import os
import numpy as np
from googletrans import Translator
import joblib


modelo_ruta = 'model/xg_model_decision_tree_regressor.pkl'

xg_model_decision_tree_regressor = joblib.load(modelo_ruta)



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
    "Introduce el nombre del jugador que desea analizar:",
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
        return  (f"> el jugador ha marcado {goals} goles en {games} partidos, asistiendo {assists} veces, ha ejecutado {pens_att} penaltis, de los cuales no marcado ninguno y los goles marcados en jugada han sido {goals_pens}.\n El resultado de los goles esperados del jugador es de {prediction[0]:.2f} goles por temporada.")

    else:
        return (f"> el jugador ha marcado {goals} goles en {games} partidos, asistiendo {assists} veces, ha ejecutado {pens_att} penaltis, de los cuales ha marcado {pens_made} y los goles marcados en jugada han sido {goals_pens}.\n El resultado de los goles esperados del jugador es de {prediction[0]:.2f} goles por temporada.")
        
      
translator = Translator()
language = "inglés"

def translate(text):
    global language
    if text != st.session_state["jugador"] and text is not None and not text.isdigit() and text!="":
        try:
            translated_text = ""
            if language == "español":
                if st.session_state["jugador"]!="":
                    text=text.replace(" "+st.session_state["jugador"]+" "," the player")
                translation = translator.translate(text, dest='es')
                translated_text = translation.text
            elif language == "inglés":
                if st.session_state["jugador"]!="":
                    text=text.replace(" "+st.session_state["jugador"]+" "," el jugador")
                translation = translator.translate(text, dest='en')
                translated_text = translation.text
            translated_text = translated_text.replace("Pie esperado", "ExpectedFoot")
            translated_text = translated_text.replace("ExpectaDfoot", "ExpectedFoot")
            if st.session_state["jugador"]!="":
                translated_text = translated_text.replace(" el jugador", " "+st.session_state["jugador"])
            if st.session_state["jugador"]!="":
                translated_text = translated_text.replace(" the player", " "+st.session_state["jugador"])
            return translated_text
        except Exception as e:
            print(f"Error en la traducción: {e}")
    else:
        return text


ruta_imagen_local = os.path.join("media", "logo.png")

st.image(ruta_imagen_local, width=400)
st.title("ExpectedFoot")

select_language_msg = translate("Selecciona el idioma: ")
spanish_option = translate("Español")
english_option = translate("Inglés")

option = st.radio("Seleccionar idioma: ",(spanish_option, english_option), key='select_language', label_visibility="hidden")

if option == spanish_option:
    language = "español"
elif option == english_option:
    language = "inglés"

if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role":"assistant", "content":translate("¡Hola! Soy el asistente de ExpectedFoot, tu analizador de jugadores.")}]
  st.session_state["messages"].append({"role":"assistant", "content":translate(correct_responses[0])})

if "messages" in st.session_state:
   for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(translate(msg["content"]))


   if user_input := st.chat_input():
     if st.session_state["messages"][-1]["role"] != "user":
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.chat_message("user").write(user_input)
        responseMessage = translate(response(user_input))
        st.session_state["messages"].append({"role": "assistant", "content": responseMessage})
        st.chat_message("assistant").write(responseMessage)
        if responseMessage==correct_responses[7]:
            newPrediction=compile_stats( st.session_state["games"],
                                        st.session_state["goals"],
                                        st.session_state["assists"],
                                        st.session_state["pens_att"], 
                                        st.session_state["pens_made"], 
                                        st.session_state["progressive_carries"])
            st.session_state["paso"]=pasos[0]
            st.session_state["messages"].append({"role": "assistant", "content":translate(newPrediction)})
            st.chat_message("assistant").write(translate(newPrediction))
            st.session_state["messages"].append({"role":"assistant", "content":translate(correct_responses[0])})
            st.chat_message("assistant").write(translate(correct_responses[0]))


