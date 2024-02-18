import streamlit as st
import os
import numpy as np
from googletrans import Translator

def contiene_solo_letras(cadena):
    return all(caracter.isalpha() or caracter.isspace() for caracter in cadena)

jugador=""
games=0
goals=0
assists=0
pens_att=0
progressive_carries=0
pens_made=0

correct_responses = [
    "Introduce el nombre del jugador que desea analizar",
  f"¿Cuántos partidos ha jugado {jugador}? ",
 f"¿Cuántos goles ha marcado el {jugador}?",
 f"¿Cuántas asistencias ha realizado el {jugador}? ",
  f"¿Cuántos penaltis ha ejecutado el {jugador}? ",
   f"¿Cuántos goles de penalti ha marcado el {jugador} de los  de los {pens_att} penaltis ejecutados?",
   "¿Cuántos avances con la pelota hacia el área ha realizado con éxito? ",
  "Analizando datos..."
]
error_responses = [
   "Por favor, introduce correctamente el nombre del jugador.",
   f"{jugador} no ha jugado ningún partido. No podemos seguir analizando a este jugador.", 
   "Error: introduzca un número natural",
   "Error: La cantidad de goles de penalti no puede ser mayor que la cantidad total de goles marcados o penaltis ejecutados.",
   ]
pasos=["nombre_jugador","partidos_jugados","goles_marcados","asistencias_realizadas","penaltis_ejecutados","goles_penaltis","avances_exito","analizando_datos"]
paso = pasos[0]

def response(user_input):
   global jugador
   global games
   global goals
   global assists
   global pens_att
   global pens_made
   global progressive_carries
   global paso
   # "Introduce el nombre del jugador que desea analizar",
   if paso==pasos[0]:
      if contiene_solo_letras(user_input):
         paso=pasos[1]
         jugador=user_input
         return correct_responses[1]
      else:
         return error_responses[0]
    #  f"¿Cuántos partidos ha jugado {jugador}? ",
   if paso==pasos[1]:
      if not user_input.isdigit():
         return error_responses[2]
      elif user_input==0:
         paso=pasos[0]
         return error_responses[1]
      else:
         paso=paso[2]
         games=user_input
         return correct_responses[2]
    # f"¿Cuántos goles ha marcado el {jugador}?",
   if paso == pasos[2]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            paso = pasos[3]
            goals = int(user_input)
            return correct_responses[3]

    # f"¿Cuántas asistencias ha realizado el {jugador}? ",
   if paso == pasos[3]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            paso = pasos[4]
            assists = int(user_input)
            return correct_responses[4]

    # f"¿Cuántos penaltis ha ejecutado el {jugador}? ",
   if paso == pasos[4]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            paso = pasos[5]
            pens_att = int(user_input)
            return correct_responses[5]

    # f"¿Cuántos goles de penalti ha marcado el {jugador} de los penaltis ejecutados? ",
   if paso == pasos[5]:
        if not user_input.isdigit() or int(user_input) > goals or int(user_input) > pens_att:
            return error_responses[3]
        else:
            paso = pasos[6]
            pens_made = int(user_input)
            return correct_responses[6]

    # "¿Cuántos avances con la pelota hacia el área ha realizado con éxito? ",
   if paso == pasos[6]:
        if not user_input.isdigit():
            return error_responses[2]
        else:
            paso = pasos[7]
            progressive_carries = int(user_input)
            return correct_responses[7]
    # "Analizando datos..."
   if paso == pasos[7]:
    paso=pasos[0]
    return compile_stats(jugador, games, goals, assists, pens_att, pens_made, progressive_carries)

def compile_stats(jugador, games, goals, assists, pens_att, pens_made, progressive_carries):  
    # Assuming you have some method to analyze these stats
    # For example:
    result = f"""
    Name: {jugador}
    Games: {games}
    Goals: {goals}
    Assists: {assists}
    Penalty Attempts: {pens_att}
    Penalty Goals: {pens_made}
    Progressive Carries: {progressive_carries}
    """
    return result
      
      

translator = Translator()
language = "inglés"

def translate(text):
    translated_text = ""
    if language == "español":
        translation = translator.translate(text, dest='es')
        translated_text = translation.text
    elif language == "inglés":
        translation = translator.translate(text, dest='en')
        translated_text = translation.text
    return translated_text


select_language_msg = translate("Selecciona el idioma: ", language)
spanish_option = translate("Español", language)
english_option = translate("Inglés", language)

option = st.sidebar.radio(select_language_msg, (spanish_option, english_option))

if option == spanish_option:
    language = "español"
elif option == english_option:
    language = "inglés"
ruta_imagen_local = os.path.join("img", "logo.png")


st.image(ruta_imagen_local, width=200)
st.title("ExpectedFoot")



if "messages" not in st.session_state:
  st.session_state["messages"] = [{"role":"assistant", "content":translate("¡Hola! Soy el asistente de ExpectedFoot, tu analizador de jugadores.")}]

if paso==pasos[0]:
    st.session_state["messages"] = [{"role":"assistant", "content":translate(correct_responses[0])}]

   
for msg in st.session_state["messages"]:
  st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
  st.session_state["messages"].append({"role": "user", "content": user_input})
  st.chat_message("user").write(user_input)
  responseMessage = translate(response(user_inputo))
  st.session_state["messages"].append({"role": "assistant", "content": responseMessage})
  st.chat_message("assistant").write(responseMessage)


