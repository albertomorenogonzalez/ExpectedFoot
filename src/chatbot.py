import numpy as np
from googletrans import Translator

translator = Translator()

def chatbot_message(user, message):
    translated_message = translate(message)
    translated_message = translated_message.replace("Pie esperado", "ExpectedFoot")
    translated_message = translated_message.replace("ExpectaDfoot", "ExpectedFoot")
    print(f"{user}: {translated_message}")

def ask_question_and_get_input(question):
    translated_question = translate(question)
    return input(f"Usuario: {translated_question} ")

def choose_language():
    while True:
        language_choice = input("Seleccione el idioma (español / inglés): ").lower()
        if language_choice in ['español', 'ingles']:
            return language_choice
        else:
            print("Por favor, seleccione un idioma válido.")

def translate(text):
    global chosen_language
    language_code = {'español': 'es', 'ingles': 'en'}
    dest_language = language_code.get(chosen_language.lower())

    if dest_language:
        translation = translator.translate(text, dest=dest_language)
        return translation.text
    else:
        print("Error: Idioma de destino no válido.")
        return text

chosen_language = choose_language()


mensaje_inicial = ("ExpectedFoot", f"¡Hola! Soy el asistente de ExpectedFoot, tu analizador de jugadores. Para comenzar, escribe 'comenzar'.")

conversation_history = []


for message in mensaje_inicial:
    chatbot_message("ExpectedFoot", message)


while True:
    start_message = input("Usuario: ")
    chatbot_message("Usuario", start_message.lower())

    if start_message.lower() == 'comenzar' or 'start':
        break
    else:
        chatbot_message("ExpectedFoot", "Para comenzar, escribe 'comenzar'.")

def contiene_solo_letras(cadena):
    return all(caracter.isalpha() or caracter.isspace() for caracter in cadena)

while True:
    user_input_message = "Introduce el nombre del jugador que desea analizar"
    translated_user_input_message = translate(user_input_message)
    player = input(f"Usuario: {translated_user_input_message} ")
    if contiene_solo_letras(player):
        break
    else:
        error_name = ("Por favor, introduce correctamente el nombre del jugador.")
        error_name_translate = translate(error_name)
        print(error_name)

chatbot_message("ExpectedFoot", f"Vamos a analizar al jugador {player}")

games = ("Usuario: ¿Cuántos partidos ha jugado el jugador? ")
translated_user_input_message = translate(games)
games = input(f"{translated_user_input_message} ")

if games == 0:
    chatbot_message("ExpectedFoot", f"{player} no ha jugado ningún partido. No podemos seguir analizando a este jugador.")
else:
    chatbot_message("ExpectedFoot", f"{player} ha jugado {games} partidos.")


goals = ("Usuario: ¿Cuántos goles ha marcado el jugador? ")
translated_user_input_message = translate(goals)
goals = int(input(f"{translated_user_input_message} "))
chatbot_message("ExpectedFoot", f"{player} ha marcado {goals} goles.")

assists = ("Usuario: ¿Cuántas asistencias ha realizado el jugador? ")
translated_user_input_message = translate(assists)
assists = int(input(f"{translated_user_input_message} "))
chatbot_message("ExpectedFoot", f"{player} ha realizado {assists} asistencias de gol.")

goals_assists = goals + assists
chatbot_message("ExpectedFoot", f"La suma de goles y asistencias juntas son {goals_assists}")

pens_att = ("Usuario: ¿Cuántos penaltis ha ejecutado el jugador? ")
translated_user_input_message = translate(pens_att)
pens_att = int(input(f"{translated_user_input_message} "))
chatbot_message("ExpectedFoot", f"{player} ha tirado {pens_att} penaltis")

while True:
    pens_made = (f"Usuario: ¿Cuántos goles de penalti ha marcado el jugador de los {pens_att} penaltis ejecutados? ")
    translated_user_input_message = translate(pens_made)
    pens_made = int(input(f"{translated_user_input_message} "))
    if 0 <= pens_made <= pens_att and pens_made <= goals:
        break
    else:
        chatbot_message("ExpectedFoot", "Error: La cantidad de goles de penalti no puede ser mayor que la cantidad total de goles marcados o penaltis ejecutados.")

goals_pens = goals - pens_made
chatbot_message("ExpectedFoot", f"Según los datos de goles de penalti, los goles marcados en jugadas son {goals_pens} goles")

progressive_carries = ("Usuario: ¿Cuántos avances con la pelota hacia el área ha realizado con éxito? ")
translated_user_input_message = translate(progressive_carries)
progressive_carries = int(input(f"{translated_user_input_message} "))
chatbot_message("ExpectedFoot", f"{player} ha regateado exitosamente {progressive_carries} veces a jugadores cerca del aerea")

new_data = [[games, goals, assists, goals_assists, pens_att, pens_made, goals_pens, progressive_carries]]

prediction = dt_model.predict(new_data)

if pens_made == 0:
    no_goal_pen = (f"{player} ha marcado {goals} goles en {games} partidos, asistiendo {assists} veces, ha ejecutado {pens_att} penaltis, de los cuales no marcado ninguno y los goles marcados en jugada han sido {goals_pens}.\n El resultado de los goles esperados del jugador es de {prediction[0]:.2f} goles por temporada")
    no_goal_pen_translate = translate(no_goal_pen)
    print(no_goal_pen)
else:
    goal_pen = (f"{player} ha marcado {goals} goles en {games} partidos, asistiendo {assists} veces, ha ejecutado {pens_att} penaltis, de los cuales ha marcado {pens_made} y los goles marcados en jugada han sido {goals_pens}.\n El resultado de los goles esperados del jugador es de {prediction[0]:.2f} goles por temporada")
    goal_pen_translate = translate(goal_pen)
    print(goal_pen)