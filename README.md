## ExpectedFoot

<p align="center">
  <img src="https://drive.google.com/uc?export=view&id=11T2jM0f9zc_rDxKuhXmZ6TlSPfGU4iyO" width=400px>
</p>

ExpectedFoot es un proyecto mediante el cual mediante datos recogidos de jugadores de las 5 grandes ligas (Liga Española, Liga Inglesa, Liga Alemana, Liga Italiana y Liga Francesa) provenientes de la web [fbref.com](https://fbref.com/en/) se encargará de predecir en base a unas estadísticas introducidas cuántos Expected Goals ('xG') que será capaz de anotar un futbolista.

Los Expected Goals ('xG') son un medida de la llamada "estadística avanzada" que se utiliza en fútbol para cuantificar la probabilidad de que un disparo a portería se convierta en gol. Un jugador con un número elevado de xG será un jugador muy a tener en cuenta, por ejemplo, Erling Haaland, uno de los mejores futbolistas y anotadores de la actualidad, tiene en la temporada actual 15 xG y 1.03 xG cada 90 minutos.

## Autores

- [Alberto Moreno González](https://github.com/albertomorenogonzalez)

- [Ciro León Espinosa Avilés](https://github.com/CiroEspinosa)

- [Francisco López González](https://github.com/franciscolg13)

## Obtención de Datos

Los datos utilizados en este proyecto son provenientes de [fbref.com](https://fbref.com/en/), una web de estadísticas históricas de clubes y jugadores de fútbol. Seleccionamos en concreto datos de las cinco ligas más importantes del mundo:

- [LaLiga](https://www.laliga.com/es-GB) - Liga Española

- [Premier League](https://www.premierleague.com/) - Liga Inglesa

- [Bundesliga](https://www.bundesliga.com/es/bundesliga) - Liga Alemana

- [Serie A](https://www.legaseriea.it/en) - Liga Italiana

- [Ligue 1](https://www.ligue1.com/) - Liga Francesa

Para obtener estos datos usaremos la técnica de web scrapping, que es es una técnica de extracción de datos que consiste en recopilar información de páginas web de forma automatizada. Utilizando programas o scripts, se analiza el contenido de las páginas para extraer datos específicos, como texto, imágenes, enlaces o cualquier otro tipo de información estructurada. Esta técnica es comúnmente utilizada para recopilar datos de múltiples fuentes en grandes cantidades para su posterior análisis, investigación o uso en aplicaciones.

En nuestro caso la utilizaremos para recopilar datos estadísticos de futbolistas desde el año 2015 hasta el año 2024 en la presente temporada.

### Scrapping

#### Análisis de la Estructura de los Datos en la Web

Primero vamos a analizar como está distribuida la página web.

![](https://drive.google.com/uc?export=view&id=1_k5Rd6DpTMtL3xe5r92X4-eK9DCz56kA)

<sub>Página de inicio</sub>

Busquemos una liga para ver como se distribuyen los datos que queremos extraer, por ejemplo, la liga española:

![](https://drive.google.com/uc?export=view&id=1Jmdy7BXCj_Nph1_QgPGR9_zX6LPpVhhq)

En el apartado destacado **Squad & Player Stats**, seleccionamos *Standard Stats*. En este apartado de cada liga es donde se encuentran los datos que queremos obtener.

![](https://drive.google.com/uc?export=view&id=1pXfMzfVMq7tu_NXgtp_6pUplKuOETPop)

Lo primero que vemos son datos generales de los equipos que no necesitamos, más abajo está lo realmente queremos obtener.

![](https://drive.google.com/uc?export=view&id=1avOvHg_f3U2p71nUoqEXEzUmxPYxaz5f)

Cada fila de esta tabla son datos de jugadores muy valiosos para el entrenamiento de nuestro modelo. Veamos como se organizan en el html.

![](https://drive.google.com/uc?export=view&id=1rVyx8zdEnFlnpYb44-ClzwRpZEiFtPYi)

Cada jugador en el html está representado por una etiqueta `tr` con todas los valores del jugador en etiquetas `td` bastante bien estructuradas para su posterior acceso. Cada etiqueta de estas esta diferenciada por el valor de un atributo que contienen llamado `data-stat`, que usaremos posteriormente para obetener los datos. Con esto en mente dirijámonos a obtener datos, no solo de este apartado de ejemplo, sino de todas aquellas temporadas de las 5 grandes ligas desde la 2010/2011 a la actual, ya que todas se organizan de la misma manera.

#### Desarrollo del Scrapping

Para obtener todos los datos necesarios para crear un modelo eficiente lo hemos hecho de la siguiente manera:

<mark><sub>**Nota**: El siguiente código es recomendable no ejecutarlo ya que el web scrapping no es una práctica que acepten la mayoría de las páginas web, sobretodo si es un número elevado de páginas como es nuestro caso. La extracción de los datos se ha hecho primero antes de insertar el código en el colab. El código se ha ejecutado cinco veces respectivamente cambiando cada liga de forma manual. La ejecución del código se ha realizado de forma cautelar y segmentada para evitar el bloqueo de la IP por parte de la web. Esta práctica se ha realizado con fines educativos, no pretendemos lucrarnos de ello.</sub></mark>


```python
# Importamos las librerías necesarias para realizar el scrapping
import re
import pandas as pd
import numpy as np
from requests import get
from bs4 import BeautifulSoup
```


```python
# La siguiente función extrará la temporada correspondiente al link actual del
# que se está scrappeando información.
def extract_season(url):
  """
  La siguiente función se encargará de extraer la temporada a la que hace
  referencia al link que se pasa como parámetro.
  """
  season_pattern = re.compile(r'https://fbref\.com/en/comps/20/(\d{4}-\d{4})/stats/\d{4}-\d{4}-(\w+)-Stats')
  matched = season_pattern.search(url)
  if matched:
      return matched.group(1)
  else:
      return None
```


```python
# Generamos una batería de URLs para comprobar si existen primero para scrappear
# La liga se cambia de forma manual, tenemos como ejemplo la Bundesliga alemana
base_url = "https://fbref.com/en/comps/20/"
urls = [base_url + f"{year}-{year+1}/stats/{year}-{year+1}-Bundesliga-Stats" for year in range(2015, 2024)]
```


```python
# Creamos un DataFrame vacío para ir almacenando los datos
combined_df = pd.DataFrame()
```

Antes de obtener los datos de cada URL tenemos que tener en cuenta una cosa. El siguiente código será de ejemplo:


```python
from requests import get

url = "https://fbref.com/en/comps/12/stats/La-Liga-Stats"

answer = get(url)

if answer.status_code == 200:
    print(answer.text)
```

La sálida de este código llegada a cierto punto será la siguiente:

![](https://drive.google.com/uc?export=view&id=1STIW3glEYDtDMi0S8j_8DMe53fDm-3Eb)

Después de realizar pruebas en las que el scrapping convencional presentaba falta de datos y muestra de la información solo hasta cierto punto, revisando el output generado de forma manual podemos observar que a partir de ciento punto en la página, la información de los jugadores está comentada, lo que hace que *BeautifulSoup* no pueda acceder a la misma. Es por eso que una vez obtenida la respuesta, simplemente eliminado las aperturas y cierres de comentarios (`<!--`, `-->`) podremos acceder a la información fácilmente. Continuemos con el código utilizado para scrappear.


```python
# Obtenemos los datos de cada URL
for url in urls:
  # Obtenemos la respuesta de una url en cada iteración
  answer = get(url)

  # Si se establecido conexión (debería ocurrir en cualquier caso)
  # obtendremos el texto de la respuesta que corresponde al
  # código html de la web. Retiramos las aperturas y cierres de
  # comentarios para poder acceder a la información fácilmente
  if answer.status_code == 200:
    answer = answer.text
    answer = answer.replace("<!--", "")
    answer = answer.replace("-->", "")

    # Parseamos el archivo con BeautifulSoup para tratarlo a continuación
    html_soup = BeautifulSoup(answer, 'html.parser')

    # Obtenemos todas las etiquetas tr, las cuáles la mayoría son datos de futbolistas
    players_html = html_soup.find_all('tr')

    # Generamos un array para atributo del jugador y añadir ahí todos los datos
    # de cada tipo para alojarlo posteriormente en el DataFrame
    # La explicación detallada de qué significan estos datos se realizará en
    # apartados posteriores.
    player = []
    team = []
    games = []
    games_starts = []
    minutes = []
    minutes_90s = []
    goals = []
    assists = []
    goals_assists = []
    goals_pens = []
    pens_made = []
    pens_att = []
    cards_yellow = []
    cards_red = []
    xg = []
    npxg = []
    xg_assist = []
    npxg_xg_assist = []
    progressive_carries = []
    progressive_passes = []
    goals_per90 = []
    assists_per90 = []
    goals_assists_per90 = []
    goals_pens_per90 = []
    goals_assists_pens_per90 = []
    xg_per90 = []
    xg_assist_per90 = []
    xg_xg_assist_per90 = []
    npxg_per90 = []
    npxg_xg_assist_per90 = []

    # Recorremos la variable que alberga las etiquetas tr, dentro de ella,
    # serán jugadores aquellos cuya primera etiqueta 'td' sea como la siguiente:
    # ''td', {'class': 'left', 'data-stat': 'player'}'. Una vez obtenida una
    # etiqueta con estos valores obtenemos cada td con atributo 'data-stat'.
    # Podemos ver esta distribución de los datos en el apartado previo donde
    # estuvimos analizándolo. Cada atributo conseguido lo guardamos en su array
    # correspondiente. Si el dato está vacío rellenamos la posicion correspondiente
    # con ''.
    for player in players_html:
      player_e = player.find('td', {'class': 'left', 'data-stat': 'player'})
      if player_e:
          player.append(player_e.text)
          team.append(player.find('td', {'class': 'left', 'data-stat': 'team'}).text)
          games.append(player.find('td', {'class': 'right group_start', 'data-stat': 'games'}).text)
          games_starts.append(player.find('td', {'data-stat': 'games_starts'}).text)
          minutes.append(player.find('td', {'data-stat': 'minutes'}).text)
          minutes_90s.append(player.find('td', {'data-stat': 'minutes_90s'}).text)
          goals.append(player.find('td', {'data-stat': 'goals'}).text if player.find('td', {'data-stat': 'goals'}) else '')
          assists.append(player.find('td', {'data-stat': 'assists'}).text if player.find('td', {'data-stat': 'assists'}) else '')
          goals_assists.append(player.find('td', {'data-stat': 'goals_assists'}).text if player.find('td', {'data-stat': 'goals_assists'}) else '')
          goals_pens.append(player.find('td', {'data-stat': 'goals_pens'}).text if player.find('td', {'data-stat': 'goals_pens'}) else '')
          pens_made.append(player.find('td', {'data-stat': 'pens_made'}).text if player.find('td', {'data-stat': 'pens_made'}) else '')
          pens_att.append(player.find('td', {'data-stat': 'pens_att'}).text if player.find('td', {'data-stat': 'pens_att'}) else '')
          cards_yellow.append(player.find('td', {'data-stat': 'cards_yellow'}).text if player.find('td', {'data-stat': 'cards_yellow'}) else '')
          cards_red.append(player.find('td', {'data-stat': 'cards_red'}).text if player.find('td', {'data-stat': 'cards_red'}) else '')
          xg.append(player.find('td', {'data-stat': 'xg'}).text if player.find('td', {'data-stat': 'xg'}) else '')
          npxg.append(player.find('td', {'data-stat': 'npxg'}).text if player.find('td', {'data-stat': 'npxg'}) else '')
          xg_assist.append(player.find('td', {'data-stat': 'xg_assist'}).text if player.find('td', {'data-stat': 'xg_assist'}) else '')
          npxg_xg_assist.append(player.find('td', {'data-stat': 'npxg_xg_assist'}).text if player.find('td', {'data-stat': 'npxg_xg_assist'}) else '')
          progressive_carries.append(player.find('td', {'data-stat': 'progressive_carries'}).text if player.find('td', {'data-stat': 'progressive_carries'}) else '')
          progressive_passes.append(player.find('td', {'data-stat': 'progressive_passes'}).text if player.find('td', {'data-stat': 'progressive_passes'}) else '')
          goals_per90.append(player.find('td', {'data-stat': 'goals_per90'}).text if player.find('td', {'data-stat': 'goals_per90'}) else '')
          assists_per90.append(player.find('td', {'data-stat': 'assists_per90'}).text if player.find('td', {'data-stat': 'assists_per90'}) else '')
          goals_assists_per90.append(player.find('td', {'data-stat': 'goals_assists_per90'}).text if player.find('td', {'data-stat': 'goals_assists_per90'}) else '')
          goals_pens_per90.append(player.find('td', {'data-stat': 'goals_pens_per90'}).text if player.find('td', {'data-stat': 'goals_pens_per90'}) else '')
          goals_assists_pens_per90.append(player.find('td', {'data-stat': 'goals_assists_pens_per90'}).text if player.find('td', {'data-stat': 'goals_assists_pens_per90'}) else '')
          xg_per90.append(player.find('td', {'data-stat': 'xg_per90'}).text if player.find('td', {'data-stat': 'xg_per90'}) else '')
          xg_assist_per90.append(player.find('td', {'data-stat': 'xg_assist_per90'}).text if player.find('td', {'data-stat': 'xg_assist_per90'}) else '')
          xg_xg_assist_per90.append(player.find('td', {'data-stat': 'xg_xg_assist_per90'}).text if player.find('td', {'data-stat': 'xg_xg_assist_per90'}) else '')
          npxg_per90.append(player.find('td', {'data-stat': 'npxg_per90'}).text if player.find('td', {'data-stat': 'npxg_per90'}) else '')
          npxg_xg_assist_per90.append(player.find('td', {'data-stat': 'npxg_xg_assist_per90'}).text if player.find('td', {'data-stat': 'npxg_xg_assist_per90'}) else '')


          # LIMPIEZA PREVIA DE LOS DATOS ANTES DE GUARDARLOS EN CSV

          # La estadística de minutos registra los valores que alacanzan los
          # miles con comas, lo que da problemas a la hora de guardarlos en
          # DataFrame. Retiramos las comas de cada valor que las contenga
          for i in range(len(minutes)):
            minutes[i] = minutes[i].replace(",", "")

          # Guardamos todos los arrays en un array
          stats = [player, team, games, games_starts, minutes, minutes_90s,
                   goals, assists, goals_assists, goals_pens, pens_made,
                   pens_att, cards_yellow, cards_red, xg, npxg, xg_assist,
                   npxg_xg_assist, progressive_carries, progressive_passes,
                   goals_per90, assists_per90, goals_assists_per90,
                   goals_pens_per90, goals_assists_pens_per90, xg_per90,
                   xg_assist_per90, xg_xg_assist_per90, npxg_per90,
                   npxg_xg_assist_per90]

          # Buscamos los valores que han quedado como '' y los transformamos a '0'
          for arr in stats:
            for i in range(len(arr)):
                if arr[i] == '':
                    arr[i] = '0'

          # Creamos un DataFrame con los datos en los que los guardamos con los
          # tipos de datos correspondientes. Si no se guardarían todos como
          # object
          data = {
              'player': player,
              # Sacamos la temporada de la URL
              'season' : extract_season(url),
              'team': team,
              'games': np.array(games).astype(int),
              'games_starts': np.array(games_starts).astype(int),
              'minutes': np.array(minutes).astype(int),
              'minutes_90s': np.array(minutes_90s).astype(np.float32),
              'goals': np.array(goals).astype(int),
              'assists': np.array(assists).astype(int),
              'goals_assists': np.array(goals_assists).astype(int),
              'goals_pens': np.array(goals_pens).astype(int),
              'pens_made': np.array(pens_made).astype(int),
              'pens_att': np.array(pens_att).astype(int),
              'cards_yellow': np.array(cards_yellow).astype(int),
              'cards_red': np.array(cards_red).astype(int),
              'xg': np.array(xg).astype(np.float32),
              'npxg': np.array(npxg).astype(np.float32),
              'xg_assist': np.array(xg_assist).astype(np.float32),
              'npxg_xg_assist': np.array(npxg_xg_assist).astype(np.float32),
              'progressive_carries': np.array(progressive_carries).astype(int),
              'progressive_passes': np.array(progressive_passes).astype(int),
              'goals_per90': np.array(goals_per90).astype(np.float32),
              'assists_per90': np.array(assists_per90).astype(np.float32),
              'goals_assists_per90': np.array(goals_assists_per90).astype(np.float32),
              'goals_pens_per90': np.array(goals_pens_per90).astype(np.float32),
              'goals_assists_pens_per90': np.array(goals_assists_pens_per90).astype(np.float32),
              'xg_per90': np.array(xg_per90).astype(np.float32),
              'xg_assist_per90': np.array(xg_assist_per90).astype(np.float32),
              'xg_xg_assist_per90': np.array(xg_xg_assist_per90).astype(np.float32),
              'npxg_per90': np.array(npxg_per90).astype(np.float32),
              'npxg_xg_assist_per90': np.array(npxg_xg_assist_per90).astype(np.float32),
          }

          df = pd.DataFrame(data)

          # Concatenamos los datos de los jugadores en la temporada en el
          # DataFrame que alberga todos los datos.
          combined_df = pd.concat([combined_df, df], ignore_index=True)


# Guardamos el DataFrame combinado en un archivo CSV
combined_df.to_csv("bundesliga_players_combined.csv", index=False)
```

### Obtención del DataFrame Unificado con el que vamos a Trabajar

Una vez obtenido los datos scrappeados para las cinco grandes ligas, han sido alojados en formato `csv` en el repositorio de GitHub del proyecto para su uso en este cuaderno de Google Colab. Para ello clonaremos el repositorio en los archivos de la máquina utilizada para ejecutar el cuaderno.


```python
# Gracias a la librería os, podemos ver si el repositorio está descargado
# o no dentro del entorno de ejecución del colab. Si no está descargado,
# lo descargará, pero si está descargado, mostrará un mensaje que lo confirma
import os

if not os.path.exists('ExpectedFoot'):
  !git clone https://github.com/albertomorenogonzalez/ExpectedFoot.git
else:
  print("El directorio ya está descargado.")
```

    Cloning into 'ExpectedFoot'...
    remote: Enumerating objects: 46, done.[K
    remote: Counting objects: 100% (46/46), done.[K
    remote: Compressing objects: 100% (39/39), done.[K
    remote: Total 46 (delta 13), reused 5 (delta 1), pack-reused 0[K
    Receiving objects: 100% (46/46), 1.33 MiB | 4.29 MiB/s, done.
    Resolving deltas: 100% (13/13), done.


Guardamos los datos de cada liga en un DataFrame distinto.


```python
import pandas as pd

bundesliga = pd.read_csv("/content/ExpectedFoot/scrap/bundesliga_players_combined.csv")
laliga = pd.read_csv("/content/ExpectedFoot/scrap/laliga_players_combined.csv")
ligue_1 = pd.read_csv("/content/ExpectedFoot/scrap/liguea_players_combined.csv")
premier_league = pd.read_csv("/content/ExpectedFoot/scrap/premierleague_players_combined.csv")
serie_a = pd.read_csv("/content/ExpectedFoot/scrap/seriea_players_combined.csv")
```

Unimos los cinco DataFrames, obteniendo todos los datos necesarios en uno solo para poder tratar los datos a partir de él.


```python
players = pd.concat([bundesliga, laliga, ligue_1, premier_league, serie_a], ignore_index=True)

players
```


      
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>David Abraham</td>
      <td>2015-2016</td>
      <td>Eint Frankfurt</td>
      <td>31</td>
      <td>28</td>
      <td>2547</td>
      <td>28.3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>René Adler</td>
      <td>2015-2016</td>
      <td>Hamburger SV</td>
      <td>24</td>
      <td>24</td>
      <td>2071</td>
      <td>23.0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.04</td>
      <td>0.04</td>
      <td>0.00</td>
      <td>0.04</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Stefan Aigner</td>
      <td>2015-2016</td>
      <td>Eint Frankfurt</td>
      <td>31</td>
      <td>27</td>
      <td>2394</td>
      <td>26.6</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>...</td>
      <td>0.11</td>
      <td>0.11</td>
      <td>0.23</td>
      <td>0.11</td>
      <td>0.23</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Albian Ajeti</td>
      <td>2015-2016</td>
      <td>Augsburg</td>
      <td>1</td>
      <td>0</td>
      <td>37</td>
      <td>0.4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>David Alaba</td>
      <td>2015-2016</td>
      <td>Bayern Munich</td>
      <td>30</td>
      <td>27</td>
      <td>2492</td>
      <td>27.7</td>
      <td>2</td>
      <td>0</td>
      <td>2</td>
      <td>...</td>
      <td>0.07</td>
      <td>0.00</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>23705</th>
      <td>Nadir Zortea</td>
      <td>2023-2024</td>
      <td>Atalanta</td>
      <td>5</td>
      <td>0</td>
      <td>149</td>
      <td>1.7</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0.60</td>
      <td>0.00</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>0.21</td>
      <td>0.05</td>
      <td>0.21</td>
    </tr>
    <tr>
      <th>23706</th>
      <td>Szymon Żurkowski</td>
      <td>2023-2024</td>
      <td>Empoli</td>
      <td>4</td>
      <td>3</td>
      <td>284</td>
      <td>3.2</td>
      <td>4</td>
      <td>0</td>
      <td>4</td>
      <td>...</td>
      <td>1.27</td>
      <td>0.00</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>0.17</td>
      <td>0.02</td>
      <td>0.18</td>
      <td>0.17</td>
      <td>0.18</td>
    </tr>
    <tr>
      <th>23707</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Hellas Verona</td>
      <td>20</td>
      <td>13</td>
      <td>1204</td>
      <td>13.4</td>
      <td>5</td>
      <td>1</td>
      <td>6</td>
      <td>...</td>
      <td>0.37</td>
      <td>0.07</td>
      <td>0.45</td>
      <td>0.30</td>
      <td>0.37</td>
      <td>0.34</td>
      <td>0.09</td>
      <td>0.43</td>
      <td>0.16</td>
      <td>0.25</td>
    </tr>
    <tr>
      <th>23708</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Monza</td>
      <td>2</td>
      <td>1</td>
      <td>124</td>
      <td>1.4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>23709</th>
      <td>Mateusz Łęgowski</td>
      <td>2023-2024</td>
      <td>Salernitana</td>
      <td>20</td>
      <td>9</td>
      <td>879</td>
      <td>9.8</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.04</td>
      <td>0.02</td>
      <td>0.04</td>
    </tr>
  </tbody>
</table>
<p>23710 rows × 31 columns</p>


## Descripción de los Datos

Ahora que tenemos todos los datos extraídos que necesitamos, vamos a describir en que consiste cada uno:


```python
players.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 23710 entries, 0 to 23709
    Data columns (total 31 columns):
     #   Column                    Non-Null Count  Dtype  
    ---  ------                    --------------  -----  
     0   player                    23710 non-null  object 
     1   season                    23710 non-null  object 
     2   team                      23710 non-null  object 
     3   games                     23710 non-null  int64  
     4   games_starts              23710 non-null  int64  
     5   minutes                   23710 non-null  int64  
     6   minutes_90s               23710 non-null  float64
     7   goals                     23710 non-null  int64  
     8   assists                   23710 non-null  int64  
     9   goals_assists             23710 non-null  int64  
     10  goals_pens                23710 non-null  int64  
     11  pens_made                 23710 non-null  int64  
     12  pens_att                  23710 non-null  int64  
     13  cards_yellow              23710 non-null  int64  
     14  cards_red                 23710 non-null  int64  
     15  xg                        23710 non-null  float64
     16  npxg                      23710 non-null  float64
     17  xg_assist                 23710 non-null  float64
     18  npxg_xg_assist            23710 non-null  float64
     19  progressive_carries       23710 non-null  int64  
     20  progressive_passes        23710 non-null  int64  
     21  goals_per90               23710 non-null  float64
     22  assists_per90             23710 non-null  float64
     23  goals_assists_per90       23710 non-null  float64
     24  goals_pens_per90          23710 non-null  float64
     25  goals_assists_pens_per90  23710 non-null  float64
     26  xg_per90                  23710 non-null  float64
     27  xg_assist_per90           23710 non-null  float64
     28  xg_xg_assist_per90        23710 non-null  float64
     29  npxg_per90                23710 non-null  float64
     30  npxg_xg_assist_per90      23710 non-null  float64
    dtypes: float64(15), int64(13), object(3)
    memory usage: 5.6+ MB


 0. `player` -> Nombre del jugador.
 1. `season` -> Temporada en la que se han recogido los datos.
 2. `team` -> Equipo al que pertenece el jugador.
 3. `games` -> Número de partidos que ha jugado el jugador en la temporada.
 4. `games_starts` -> Número de partidos que el jugador ha jugado de titular.
 5. `minutes` -> Minutos que ha jugado el jugador durante la temporada.
 6. `minutes_90s` -> Minutos jugados divididos entre 90.
 7. `goals` -> Goles anotados por el jugador.
 8. `assists` -> Asistencias realizadas por el jugador.
 9. `goals_assist` -> Goles y asistencias sumadas.
 10. `goals_pens` -> Goles que no han sido lanzamientos de penalti.
 11. `pens_made` -> Goles anotados de lanzamiento de penalti por el jugador.
 12. `pens_att` -> Lanzamientos de penalti intentados por el jugador.
 13. `cards_yellow` -> Tarjetas amarillas que ha visto el jugador.
 14. `cards_red` -> Tarjetas rojas que ha visto el jugador.
 15. `xg` **-> Expected Goals**
 16. `npxg` -> Expected Goals sin contar los lanzamientos de penalti.
 17. `xg_assists` -> Asistencias esperadas.
 18. `npxg_xg_assist` -> Suma de `npxg` y `xg_assists`.
 19. `progressive_carries` -> Avances progresivos, intentos exitosos de avance hacia adelante por parte de un jugador en los últimos 10 metros de campo.
 20. `progressive_passes` -> Pases progresivos, aquellos pases que mueven hacia la línea de gol en los últimos 10 metros de campo.
 21. `goals_per90` -> Goles anotados por un jugador cada 90 minutos.
 22. `assist_per90` -> Asistencias realizadas por el jugador cada 90 minutos.
 23. `goals_assists_per90` -> Suma de goles y asistencias cada 90 minutos.
 24. `goals_pens_per90` -> Goles sin contar penaltis anotados por parte del jugador cada 90 minutos.
 25. `goals_assists_pens_per90` -> Suma de goles sin contar penaltis y asistencias cada 90 minutos.
 26. `xg_per90` -> Expected Goals cada 90 minutos.
 27. `xg_assist_per90` -> Asistencias esperadas cada 90 minutos.
 28. `xg_xg_assist_per90` -> Suma de Goles y Asistencias esperados cada 90 minutos.
 29. `npxg_per90` -> Expected Goals sin contar penaltis cada 90 minutos.
 30. `npxg_xg_assist_per90` -> Suma de `npxg` y `xg_assists` cada 90 minutos.

## Exploración y Visualización de los Datos

Ahora que tenemos los datos y sabemos en qué consisten, vamos a analizar como están distribuidos para hacer un cambio posterior si es necesario.


```python
players.head()
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>David Abraham</td>
      <td>2015-2016</td>
      <td>Eint Frankfurt</td>
      <td>31</td>
      <td>28</td>
      <td>2547</td>
      <td>28.3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>René Adler</td>
      <td>2015-2016</td>
      <td>Hamburger SV</td>
      <td>24</td>
      <td>24</td>
      <td>2071</td>
      <td>23.0</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.04</td>
      <td>0.04</td>
      <td>0.00</td>
      <td>0.04</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Stefan Aigner</td>
      <td>2015-2016</td>
      <td>Eint Frankfurt</td>
      <td>31</td>
      <td>27</td>
      <td>2394</td>
      <td>26.6</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>...</td>
      <td>0.11</td>
      <td>0.11</td>
      <td>0.23</td>
      <td>0.11</td>
      <td>0.23</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Albian Ajeti</td>
      <td>2015-2016</td>
      <td>Augsburg</td>
      <td>1</td>
      <td>0</td>
      <td>37</td>
      <td>0.4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>David Alaba</td>
      <td>2015-2016</td>
      <td>Bayern Munich</td>
      <td>30</td>
      <td>27</td>
      <td>2492</td>
      <td>27.7</td>
      <td>2</td>
      <td>0</td>
      <td>2</td>
      <td>...</td>
      <td>0.07</td>
      <td>0.00</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 31 columns</p>


```python
players.tail()
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23705</th>
      <td>Nadir Zortea</td>
      <td>2023-2024</td>
      <td>Atalanta</td>
      <td>5</td>
      <td>0</td>
      <td>149</td>
      <td>1.7</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0.60</td>
      <td>0.00</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>0.21</td>
      <td>0.05</td>
      <td>0.21</td>
    </tr>
    <tr>
      <th>23706</th>
      <td>Szymon Żurkowski</td>
      <td>2023-2024</td>
      <td>Empoli</td>
      <td>4</td>
      <td>3</td>
      <td>284</td>
      <td>3.2</td>
      <td>4</td>
      <td>0</td>
      <td>4</td>
      <td>...</td>
      <td>1.27</td>
      <td>0.00</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>0.17</td>
      <td>0.02</td>
      <td>0.18</td>
      <td>0.17</td>
      <td>0.18</td>
    </tr>
    <tr>
      <th>23707</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Hellas Verona</td>
      <td>20</td>
      <td>13</td>
      <td>1204</td>
      <td>13.4</td>
      <td>5</td>
      <td>1</td>
      <td>6</td>
      <td>...</td>
      <td>0.37</td>
      <td>0.07</td>
      <td>0.45</td>
      <td>0.30</td>
      <td>0.37</td>
      <td>0.34</td>
      <td>0.09</td>
      <td>0.43</td>
      <td>0.16</td>
      <td>0.25</td>
    </tr>
    <tr>
      <th>23708</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Monza</td>
      <td>2</td>
      <td>1</td>
      <td>124</td>
      <td>1.4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>23709</th>
      <td>Mateusz Łęgowski</td>
      <td>2023-2024</td>
      <td>Salernitana</td>
      <td>20</td>
      <td>9</td>
      <td>879</td>
      <td>9.8</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.04</td>
      <td>0.02</td>
      <td>0.04</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 31 columns</p>


Si nos fijamos bien podemos ver el primer problema que existe con los datos ya en esta visualización previa de algunas filas, pero antes vamos a ver su distribución y formato.


```python
players.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 23710 entries, 0 to 23709
    Data columns (total 31 columns):
     #   Column                    Non-Null Count  Dtype  
    ---  ------                    --------------  -----  
     0   player                    23710 non-null  object 
     1   season                    23710 non-null  object 
     2   team                      23710 non-null  object 
     3   games                     23710 non-null  int64  
     4   games_starts              23710 non-null  int64  
     5   minutes                   23710 non-null  int64  
     6   minutes_90s               23710 non-null  float64
     7   goals                     23710 non-null  int64  
     8   assists                   23710 non-null  int64  
     9   goals_assists             23710 non-null  int64  
     10  goals_pens                23710 non-null  int64  
     11  pens_made                 23710 non-null  int64  
     12  pens_att                  23710 non-null  int64  
     13  cards_yellow              23710 non-null  int64  
     14  cards_red                 23710 non-null  int64  
     15  xg                        23710 non-null  float64
     16  npxg                      23710 non-null  float64
     17  xg_assist                 23710 non-null  float64
     18  npxg_xg_assist            23710 non-null  float64
     19  progressive_carries       23710 non-null  int64  
     20  progressive_passes        23710 non-null  int64  
     21  goals_per90               23710 non-null  float64
     22  assists_per90             23710 non-null  float64
     23  goals_assists_per90       23710 non-null  float64
     24  goals_pens_per90          23710 non-null  float64
     25  goals_assists_pens_per90  23710 non-null  float64
     26  xg_per90                  23710 non-null  float64
     27  xg_assist_per90           23710 non-null  float64
     28  xg_xg_assist_per90        23710 non-null  float64
     29  npxg_per90                23710 non-null  float64
     30  npxg_xg_assist_per90      23710 non-null  float64
    dtypes: float64(15), int64(13), object(3)
    memory usage: 5.6+ MB


Afortunadamente no tenemos valores nulos en nuestros datos (en este caso particular de fútbol, si una estadística no tiene valor este es igual a 0). Los únicos valores que no son númericos, ya sea `int` o `float` son: el nombre del jugador, la temporada y el equipo al que pertenece el futbolista, Estos datos en un principio no contarían para el entrenamiento, el nombre del jugador debería ser sustituido por un id numérico si se fuese a tener en cuenta. En las 14 temporadas de las que hemos obtenido registros hay una gran cantidad de equipos que será difícil de sustituir, además de que la calidad colectiva de un equipo no tiene por qué afectar a la calidad individual de un jugador, sea o no sea exitoso el club. La temporada tampoco parece ser relevante.

Los registros pertenecientes a la estadística avanzada (`npxg`,
`xg_assists`, `npxg_xg_assist`, `xg_per90`, `xg_assist_per90`, `xg_xg_assist_per90`, `npxg_per90`, `npxg_xg_assist_per90`) ya que son calculados a través del resto para ser visualizados al igual que `xg` que es el que nos interesa, no serán tenidos en cuenta a la hora de realizar el entrenamiento con total seguridad, independientemente de su correlación. La idea es realizar la predicción con datos convencionales. Para poder averiguar el resto de datos deberíamos hacer un modelo de IA para cada uno.

`xg` es el dato que queremos predecir. Veamos cuáles son los 10 jugadores en cualquier temporada que más alta tienen esta estadística.


```python
best_players_xg = players.sort_values(by='xg', ascending=False)

top_10_players = best_players_xg.head(10).copy()

top_10_players
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>3196</th>
      <td>Robert Lewandowski</td>
      <td>2021-2022</td>
      <td>Bayern Munich</td>
      <td>34</td>
      <td>34</td>
      <td>2946</td>
      <td>32.7</td>
      <td>35</td>
      <td>3</td>
      <td>38</td>
      <td>...</td>
      <td>1.07</td>
      <td>0.09</td>
      <td>1.16</td>
      <td>0.92</td>
      <td>1.01</td>
      <td>1.01</td>
      <td>0.13</td>
      <td>1.15</td>
      <td>0.90</td>
      <td>1.03</td>
    </tr>
    <tr>
      <th>2695</th>
      <td>Robert Lewandowski</td>
      <td>2020-2021</td>
      <td>Bayern Munich</td>
      <td>29</td>
      <td>28</td>
      <td>2458</td>
      <td>27.3</td>
      <td>41</td>
      <td>7</td>
      <td>48</td>
      <td>...</td>
      <td>1.50</td>
      <td>0.26</td>
      <td>1.76</td>
      <td>1.21</td>
      <td>1.46</td>
      <td>1.14</td>
      <td>0.17</td>
      <td>1.31</td>
      <td>0.88</td>
      <td>1.06</td>
    </tr>
    <tr>
      <th>1721</th>
      <td>Robert Lewandowski</td>
      <td>2018-2019</td>
      <td>Bayern Munich</td>
      <td>33</td>
      <td>33</td>
      <td>2957</td>
      <td>32.9</td>
      <td>22</td>
      <td>7</td>
      <td>29</td>
      <td>...</td>
      <td>0.67</td>
      <td>0.21</td>
      <td>0.88</td>
      <td>0.58</td>
      <td>0.79</td>
      <td>0.93</td>
      <td>0.27</td>
      <td>1.21</td>
      <td>0.84</td>
      <td>1.11</td>
    </tr>
    <tr>
      <th>2189</th>
      <td>Robert Lewandowski</td>
      <td>2019-2020</td>
      <td>Bayern Munich</td>
      <td>31</td>
      <td>31</td>
      <td>2759</td>
      <td>30.7</td>
      <td>34</td>
      <td>4</td>
      <td>38</td>
      <td>...</td>
      <td>1.11</td>
      <td>0.13</td>
      <td>1.24</td>
      <td>0.95</td>
      <td>1.08</td>
      <td>1.00</td>
      <td>0.22</td>
      <td>1.22</td>
      <td>0.87</td>
      <td>1.09</td>
    </tr>
    <tr>
      <th>21164</th>
      <td>Cristiano Ronaldo</td>
      <td>2019-2020</td>
      <td>Juventus</td>
      <td>33</td>
      <td>33</td>
      <td>2917</td>
      <td>32.4</td>
      <td>31</td>
      <td>5</td>
      <td>36</td>
      <td>...</td>
      <td>0.96</td>
      <td>0.15</td>
      <td>1.11</td>
      <td>0.59</td>
      <td>0.74</td>
      <td>0.88</td>
      <td>0.20</td>
      <td>1.08</td>
      <td>0.57</td>
      <td>0.76</td>
    </tr>
    <tr>
      <th>17505</th>
      <td>Erling Haaland</td>
      <td>2022-2023</td>
      <td>Manchester City</td>
      <td>35</td>
      <td>33</td>
      <td>2769</td>
      <td>30.8</td>
      <td>36</td>
      <td>8</td>
      <td>44</td>
      <td>...</td>
      <td>1.17</td>
      <td>0.26</td>
      <td>1.43</td>
      <td>0.94</td>
      <td>1.20</td>
      <td>0.92</td>
      <td>0.17</td>
      <td>1.09</td>
      <td>0.75</td>
      <td>0.92</td>
    </tr>
    <tr>
      <th>10481</th>
      <td>Kylian Mbappé</td>
      <td>2018-2019</td>
      <td>Paris S-G</td>
      <td>29</td>
      <td>24</td>
      <td>2343</td>
      <td>26.0</td>
      <td>33</td>
      <td>7</td>
      <td>40</td>
      <td>...</td>
      <td>1.27</td>
      <td>0.27</td>
      <td>1.54</td>
      <td>1.23</td>
      <td>1.50</td>
      <td>1.08</td>
      <td>0.21</td>
      <td>1.28</td>
      <td>1.01</td>
      <td>1.22</td>
    </tr>
    <tr>
      <th>1251</th>
      <td>Robert Lewandowski</td>
      <td>2017-2018</td>
      <td>Bayern Munich</td>
      <td>30</td>
      <td>24</td>
      <td>2172</td>
      <td>24.1</td>
      <td>29</td>
      <td>2</td>
      <td>31</td>
      <td>...</td>
      <td>1.20</td>
      <td>0.08</td>
      <td>1.28</td>
      <td>0.95</td>
      <td>1.04</td>
      <td>1.16</td>
      <td>0.10</td>
      <td>1.26</td>
      <td>0.93</td>
      <td>1.03</td>
    </tr>
    <tr>
      <th>21781</th>
      <td>Cristiano Ronaldo</td>
      <td>2020-2021</td>
      <td>Juventus</td>
      <td>33</td>
      <td>31</td>
      <td>2802</td>
      <td>31.1</td>
      <td>29</td>
      <td>2</td>
      <td>31</td>
      <td>...</td>
      <td>0.93</td>
      <td>0.06</td>
      <td>1.00</td>
      <td>0.74</td>
      <td>0.80</td>
      <td>0.89</td>
      <td>0.12</td>
      <td>1.01</td>
      <td>0.69</td>
      <td>0.81</td>
    </tr>
    <tr>
      <th>20941</th>
      <td>Ciro Immobile</td>
      <td>2019-2020</td>
      <td>Lazio</td>
      <td>37</td>
      <td>36</td>
      <td>3170</td>
      <td>35.2</td>
      <td>36</td>
      <td>9</td>
      <td>45</td>
      <td>...</td>
      <td>1.02</td>
      <td>0.26</td>
      <td>1.28</td>
      <td>0.62</td>
      <td>0.88</td>
      <td>0.77</td>
      <td>0.18</td>
      <td>0.95</td>
      <td>0.44</td>
      <td>0.61</td>
    </tr>
  </tbody>
</table>
<p>10 rows × 31 columns</p>



También podemos ver estos datos en una gráfica:


```python
import matplotlib.pyplot as plt
import seaborn as sns

top_10_players['position'] = range(1, len(top_10_players) + 1)

top_10_players.loc[:, 'player-season'] = top_10_players.apply(lambda row: f"{row['position']}. {row['player']} - {row['season']}", axis=1)

plt.figure(figsize=(15, 8))
ax = sns.barplot(x='xg', y='player-season', hue='player-season', data=top_10_players, palette='crest', dodge=False)

for bar in ax.patches:
    width = bar.get_width()
    ax.text(width + 0.4, bar.get_y() + bar.get_height()/2, f'{width}', ha='left', va='center')

plt.xlabel('xG')
plt.ylabel('Jugador - Temporada')
plt.title('Top 10 jugadores con mayor número de goles esperados (xG)')
plt.show()
```


    
![Top 10 jugadores con mayor número de goles esperados (xG)](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_55_0.png)
    


Estos son los jugadores con mayor número de xG en una temporada desde la temporada 2010-2011 hasta la actualidad. Todos ellos son delanteros, haciendo obvio que los jugadores de esta posición son los que van a tener valores más altos en esta estadística. Veamos cuantos goles ha marcado cada uno de estos jugadores.


```python
plt.figure(figsize=(15, 8))
ax = sns.barplot(x='goals', y='player-season', hue='player-season', data=top_10_players, palette='crest', dodge=False)

for bar in ax.patches:
    width = bar.get_width()
    ax.text(width + 0.4, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='left', va='center')

plt.xlabel('Goles')
plt.ylabel('Jugador - Temporada')
plt.title('Números de Goles del Top 10 jugadores con mayor número de goles esperados (xG)')
plt.show()
```


    
![Números de Goles del Top 10 jugadores con mayor número de goles esperados (xG)](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_57_0.png)
    


Vemos como los xG no se corresponden con los goles anotados, los jugadores pueden superar esta espectativa o no alcanzarla. Al ser de los mejores delanteros del mundo se espera que la superen o al menos la igualen. Podemos observar como solo hay un caso en el que no se han superado espectativas y es Robert Lewandowski en la temporada 2018/2019, que es el tercer valor de xG más alto. ¿Qué ha podido influir en esto? Tenemos claro que la estadística que buscamos depende de muchos más factores que no son los goles. Veamos las estadísticas del jugador sin contar las avanzadas ni las de cada 90 minutos:


```python
top_10_players[top_10_players['position'] == 3][["player", "season", "games", "games_starts", "minutes", "goals", "assists", "goals_assists", "goals_pens", "pens_made", "pens_att", "cards_yellow", "cards_red", "progressive_carries", "progressive_passes"]]
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_made</th>
      <th>pens_att</th>
      <th>cards_yellow</th>
      <th>cards_red</th>
      <th>progressive_carries</th>
      <th>progressive_passes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1721</th>
      <td>Robert Lewandowski</td>
      <td>2018-2019</td>
      <td>33</td>
      <td>33</td>
      <td>2957</td>
      <td>22</td>
      <td>7</td>
      <td>29</td>
      <td>19</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>0</td>
      <td>79</td>
      <td>92</td>
    </tr>
  </tbody>
</table>



El jugador estuvo presente siendo titular en 33 de las 34 jornadas que componen la bundesliga, dio 7 asistencias y de los 22 goles que anotó, 3 fueron de penalti, habiendo tirado 4. El futbolista realizó 79 avances progresivos a portería y dio un total de 92 pases en los últimos 10 metros de campo. Comparemos ahora con el segundo valor de xG más alto (31.3) que también lo consigue Robert Lewandowski, pero en la temporada 2020/2021 y donde supera espectativas con creces (41 goles anotados).


```python
top_10_players[top_10_players['position'] == 2][["player", "season", "games", "games_starts", "minutes", "goals", "assists", "goals_assists", "goals_pens", "pens_made", "pens_att", "cards_yellow", "cards_red", "progressive_carries", "progressive_passes"]]
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_made</th>
      <th>pens_att</th>
      <th>cards_yellow</th>
      <th>cards_red</th>
      <th>progressive_carries</th>
      <th>progressive_passes</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2695</th>
      <td>Robert Lewandowski</td>
      <td>2020-2021</td>
      <td>29</td>
      <td>28</td>
      <td>2458</td>
      <td>41</td>
      <td>7</td>
      <td>48</td>
      <td>33</td>
      <td>8</td>
      <td>9</td>
      <td>4</td>
      <td>0</td>
      <td>51</td>
      <td>67</td>
    </tr>
  </tbody>
</table>



La temporada 2019/2020 fue redonda para el jugador. Jugando 4 partidos menos, marcó casi el doble de goles, de los cuales 8 de ellos fueron de penalti. El jugador realizó 51 avances progresivos, 28 menos que en la 2018/2019 y 67 pases en los últimos 10 metros de campo, 25 menos que en la temporada anterior. Con esto podemos observar que la estadística de los goles esperados tiene que ver más con la efectividad que puede tener el jugador de cara a portería más que con el aporte que este realice posteriormente. Veamos los avances y pases progresivos que tiene el top 10 de jugadores con más xG.


```python
plt.figure(figsize=(15, 8))
ax = sns.barplot(x='progressive_carries', y='player-season', hue='player-season', data=top_10_players, palette='crest', dodge=False)

for bar in ax.patches:
    width = bar.get_width()
    ax.text(width + 0.4, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='left', va='center')

plt.xlabel('Avances Progresivos')
plt.ylabel('Jugador - Temporada')
plt.title('Números de Avances Progresivos del Top 10 jugadores con mayor número de goles esperados (xG)')
plt.show()
```


    
![Números de Avances Progresivos del Top 10 jugadores con mayor número de goles esperados (xG)](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_63_0.png)
    



```python
plt.figure(figsize=(15, 8))
ax = sns.barplot(x='progressive_passes', y='player-season', hue='player-season', data=top_10_players, palette='crest', dodge=False)

for bar in ax.patches:
    width = bar.get_width()
    ax.text(width + 0.4, bar.get_y() + bar.get_height()/2, f'{int(width)}', ha='left', va='center')

plt.xlabel('Pases Progresivos')
plt.ylabel('Jugador - Temporada')
plt.title('Números de Pases Progresivos del Top 10 jugadores con mayor número de goles esperados (xG)')
plt.show()
```


    
![Números de Pases Progresivos del Top 10 jugadores con mayor número de goles esperados (xG)](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_64_0.png)
    


 En el caso de los avances progresivos, su relación con los xG podría corresponderse con el número de goles que han provenido de estos. No sería con el porcentaje de efectividad ya que vemos que Cristiano Ronaldo tiene un gran número de avances y pases progresivos, haciendo que la comparación entre esta estadística y sus goles sea baja. Luego tenemos el caso de Haaland, con 36 goles y 35 avances progresivos. Esto podría deberse a que sus goles no han venido de avances si no de remates o lanzamientos de penalti. Esto hace que la relación entre xG y progressive carries no sea tan clara. En general, a la hora de contar con los pases progresivos, no todo pase dado en los últimos 10 metros de campo tiene que acabar en gol ya que una parte importante de ellos no depende del jugador al ser más probable en ese caso realizar una asistencia. La relación real entre todas estas estadísticas la veranos a la hora de ver la correlación de los datos. También es curioso el caso de estos números son de las últimas 6 temporadas solamente. Veamos por qué realizando la media de los xG por temporada.


```python
players.groupby('season')['xg'].mean()
```




    season
    2015-2016    0.000000
    2016-2017    0.000000
    2017-2018    1.805425
    2018-2019    1.925489
    2019-2020    1.778843
    2020-2021    1.766513
    2021-2022    1.689829
    2022-2023    1.781029
    2023-2024    1.105680
    Name: xg, dtype: float64



La media de las temporadas 2015/2016 y 2016/2017 es 0, lo que implica que no hay registros de Expected Goals en la página para esos años. También vemos como la media de la temporada actual es más baja, ya que aún no ha terminado.

Además de todo esto, vamos a volver a ver el `.tail()` del DataFrame, ya que si nos fijamos bien, existe un caso a destacar.


```python
players.tail()
```



</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>23705</th>
      <td>Nadir Zortea</td>
      <td>2023-2024</td>
      <td>Atalanta</td>
      <td>5</td>
      <td>0</td>
      <td>149</td>
      <td>1.7</td>
      <td>1</td>
      <td>0</td>
      <td>1</td>
      <td>...</td>
      <td>0.60</td>
      <td>0.00</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.05</td>
      <td>0.16</td>
      <td>0.21</td>
      <td>0.05</td>
      <td>0.21</td>
    </tr>
    <tr>
      <th>23706</th>
      <td>Szymon Żurkowski</td>
      <td>2023-2024</td>
      <td>Empoli</td>
      <td>4</td>
      <td>3</td>
      <td>284</td>
      <td>3.2</td>
      <td>4</td>
      <td>0</td>
      <td>4</td>
      <td>...</td>
      <td>1.27</td>
      <td>0.00</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>0.17</td>
      <td>0.02</td>
      <td>0.18</td>
      <td>0.17</td>
      <td>0.18</td>
    </tr>
    <tr>
      <th>23707</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Hellas Verona</td>
      <td>20</td>
      <td>13</td>
      <td>1204</td>
      <td>13.4</td>
      <td>5</td>
      <td>1</td>
      <td>6</td>
      <td>...</td>
      <td>0.37</td>
      <td>0.07</td>
      <td>0.45</td>
      <td>0.30</td>
      <td>0.37</td>
      <td>0.34</td>
      <td>0.09</td>
      <td>0.43</td>
      <td>0.16</td>
      <td>0.25</td>
    </tr>
    <tr>
      <th>23708</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Monza</td>
      <td>2</td>
      <td>1</td>
      <td>124</td>
      <td>1.4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
    </tr>
    <tr>
      <th>23709</th>
      <td>Mateusz Łęgowski</td>
      <td>2023-2024</td>
      <td>Salernitana</td>
      <td>20</td>
      <td>9</td>
      <td>879</td>
      <td>9.8</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.02</td>
      <td>0.02</td>
      <td>0.04</td>
      <td>0.02</td>
      <td>0.04</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 31 columns</p>




Podemos observar un mismo jugador en una misma temporada con datos en dos clubes distintos. Tenemos datos para un mismo jugador en distintas temporadas pero también existe el caso de que ese jugador haya cambiado de equipo en el mercado de fichajes de invierno, haciendo que sus datos estén divididos. Veamos cuantos datos pertenecen a este mismo caso:


```python
unique = []
repeated = []

for index, row in players.iterrows():
    player = row['player']
    season = row['season']
    element = (player, season)
    if element in unique:
        repeated.append(element)
    else:
        unique.append(element)

print("Valores repetidos en el dataset:", len(repeated))
```

    Valores repetidos en el dataset: 1138



```python
repeated_df = pd.DataFrame(repeated, columns=['player', 'season'])
repeated_df.tail(10)
```



</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1128</th>
      <td>Roberto Piccoli</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1129</th>
      <td>Demba Seck</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1130</th>
      <td>Filippo Terracciano</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1131</th>
      <td>Vitinha</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1132</th>
      <td>Mateusz Wieteska</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1133</th>
      <td>Alessandro Zanoli</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1134</th>
      <td>Duván Zapata</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1135</th>
      <td>Alessio Zerbin</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1136</th>
      <td>Nadir Zortea</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1137</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
    </tr>
  </tbody>
</table>




Aquí podemos ver algunos de los jugadores que han cambiado de club en el presente mercado de invierno al aparecer dos veces en esta temporada. ¿Qué hacemos con estos datos? Podríamos juntarlos pero ocurren tres problemas, y veamoslo con un ejemplo:


```python
repeated_df[repeated_df['player'] == 'Vitinha']
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>418</th>
      <td>Vitinha</td>
      <td>2022-2023</td>
    </tr>
    <tr>
      <th>440</th>
      <td>Vitinha</td>
      <td>2023-2024</td>
    </tr>
    <tr>
      <th>1131</th>
      <td>Vitinha</td>
      <td>2023-2024</td>
    </tr>
  </tbody>
</table>



```python
players[players['player'] == 'Vitinha']
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>13020</th>
      <td>Vitinha</td>
      <td>2022-2023</td>
      <td>Marseille</td>
      <td>14</td>
      <td>5</td>
      <td>464</td>
      <td>5.2</td>
      <td>2</td>
      <td>0</td>
      <td>2</td>
      <td>...</td>
      <td>0.39</td>
      <td>0.00</td>
      <td>0.39</td>
      <td>0.39</td>
      <td>0.39</td>
      <td>0.77</td>
      <td>0.03</td>
      <td>0.80</td>
      <td>0.77</td>
      <td>0.80</td>
    </tr>
    <tr>
      <th>13021</th>
      <td>Vitinha</td>
      <td>2022-2023</td>
      <td>Paris S-G</td>
      <td>36</td>
      <td>29</td>
      <td>2446</td>
      <td>27.2</td>
      <td>2</td>
      <td>3</td>
      <td>5</td>
      <td>...</td>
      <td>0.07</td>
      <td>0.11</td>
      <td>0.18</td>
      <td>0.07</td>
      <td>0.18</td>
      <td>0.11</td>
      <td>0.11</td>
      <td>0.22</td>
      <td>0.11</td>
      <td>0.22</td>
    </tr>
    <tr>
      <th>13529</th>
      <td>Vitinha</td>
      <td>2023-2024</td>
      <td>Marseille</td>
      <td>18</td>
      <td>10</td>
      <td>923</td>
      <td>10.3</td>
      <td>3</td>
      <td>2</td>
      <td>5</td>
      <td>...</td>
      <td>0.29</td>
      <td>0.20</td>
      <td>0.49</td>
      <td>0.29</td>
      <td>0.49</td>
      <td>0.50</td>
      <td>0.28</td>
      <td>0.78</td>
      <td>0.50</td>
      <td>0.78</td>
    </tr>
    <tr>
      <th>13530</th>
      <td>Vitinha</td>
      <td>2023-2024</td>
      <td>Paris S-G</td>
      <td>19</td>
      <td>15</td>
      <td>1377</td>
      <td>15.3</td>
      <td>5</td>
      <td>2</td>
      <td>7</td>
      <td>...</td>
      <td>0.33</td>
      <td>0.13</td>
      <td>0.46</td>
      <td>0.33</td>
      <td>0.46</td>
      <td>0.14</td>
      <td>0.15</td>
      <td>0.29</td>
      <td>0.14</td>
      <td>0.29</td>
    </tr>
    <tr>
      <th>16704</th>
      <td>Vitinha</td>
      <td>2020-2021</td>
      <td>Wolves</td>
      <td>19</td>
      <td>5</td>
      <td>520</td>
      <td>5.8</td>
      <td>0</td>
      <td>1</td>
      <td>1</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.17</td>
      <td>0.17</td>
      <td>0.00</td>
      <td>0.17</td>
      <td>0.09</td>
      <td>0.11</td>
      <td>0.20</td>
      <td>0.09</td>
      <td>0.20</td>
    </tr>
    <tr>
      <th>23675</th>
      <td>Vitinha</td>
      <td>2023-2024</td>
      <td>Genoa</td>
      <td>1</td>
      <td>0</td>
      <td>14</td>
      <td>0.2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.65</td>
      <td>0.00</td>
      <td>0.65</td>
      <td>0.65</td>
      <td>0.65</td>
    </tr>
  </tbody>
</table>
<p>6 rows × 31 columns</p>



Si después de haber filtrado qué jugadores tienen varias entradas para una temporada y tenemos para una temporada aún dos jugadores con el mismo nombre, después de comprobar su trayectoria podemos comprobar que son dos jugadores distintos. Si fuésemos a juntar todas las entradas con mismo nombre y mismo temporada nos encontramos con dos problemas:

- Jugadores con el mismo nombre, siendo este el único valor que diferencia a un jugador junto con la temporada.

- Al cambiar de equipo un jugador, su rol también cambia, haciendo que las oportunidades de lanzamiento a puerta cambien también además de los xG. Por lo tanto, sumar ambos valor de xG sería impreciso.

Después de analizar estos datos, veamos la información que nos aporta `.describe()`


```python
players.describe()
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_made</th>
      <th>pens_att</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>...</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
      <td>23710.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>18.143863</td>
      <td>13.863475</td>
      <td>1244.731379</td>
      <td>13.830316</td>
      <td>1.698482</td>
      <td>1.180219</td>
      <td>2.878701</td>
      <td>1.540827</td>
      <td>0.157655</td>
      <td>0.201392</td>
      <td>...</td>
      <td>0.114005</td>
      <td>0.084202</td>
      <td>0.198227</td>
      <td>0.105663</td>
      <td>0.189871</td>
      <td>0.102936</td>
      <td>0.069567</td>
      <td>0.172514</td>
      <td>0.096103</td>
      <td>0.165689</td>
    </tr>
    <tr>
      <th>std</th>
      <td>11.323856</td>
      <td>11.209328</td>
      <td>969.779586</td>
      <td>10.775287</td>
      <td>3.287864</td>
      <td>1.957873</td>
      <td>4.665690</td>
      <td>2.903265</td>
      <td>0.713289</td>
      <td>0.842464</td>
      <td>...</td>
      <td>0.402762</td>
      <td>0.326200</td>
      <td>0.529078</td>
      <td>0.396748</td>
      <td>0.523408</td>
      <td>0.366352</td>
      <td>0.194873</td>
      <td>0.431403</td>
      <td>0.361064</td>
      <td>0.425668</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>8.000000</td>
      <td>3.000000</td>
      <td>339.000000</td>
      <td>3.800000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>18.000000</td>
      <td>12.000000</td>
      <td>1108.000000</td>
      <td>12.300000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.080000</td>
      <td>0.000000</td>
      <td>0.080000</td>
      <td>0.030000</td>
      <td>0.020000</td>
      <td>0.080000</td>
      <td>0.030000</td>
      <td>0.080000</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>28.000000</td>
      <td>23.000000</td>
      <td>2009.000000</td>
      <td>22.300000</td>
      <td>2.000000</td>
      <td>2.000000</td>
      <td>4.000000</td>
      <td>2.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>...</td>
      <td>0.150000</td>
      <td>0.110000</td>
      <td>0.280000</td>
      <td>0.130000</td>
      <td>0.270000</td>
      <td>0.120000</td>
      <td>0.100000</td>
      <td>0.250000</td>
      <td>0.120000</td>
      <td>0.240000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>38.000000</td>
      <td>38.000000</td>
      <td>3420.000000</td>
      <td>38.000000</td>
      <td>41.000000</td>
      <td>21.000000</td>
      <td>57.000000</td>
      <td>37.000000</td>
      <td>14.000000</td>
      <td>15.000000</td>
      <td>...</td>
      <td>45.000000</td>
      <td>18.000000</td>
      <td>45.000000</td>
      <td>45.000000</td>
      <td>45.000000</td>
      <td>42.660000</td>
      <td>10.060000</td>
      <td>42.660000</td>
      <td>42.660000</td>
      <td>42.660000</td>
    </tr>
  </tbody>
</table>
<p>8 rows × 28 columns</p>



```python
players.hist(bins=50, figsize=(20, 15))
plt.show()
```


    
![players.hist](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_79_0.png)
    


Después de la descripción de los datos y la muestra de los histogramas podemos observar varias cosas:

- Todos los histogramas tienen colas alargadas hacia la izquierda, lo que implica un gran número de valores bajos, siendo pocos los jugadores que despuntan.

- En las estadísticas orientadas a 90 minutos hay muchos valores a 0 o cerca. Esto se debe a que los valores comprenden números entre 0 y 2 o 3 como mucho.

- En las estadísticas avanzadas (expected) tenemos el mismo problema que en las estadísticas orientadas a 90 minutos ya que comprenden únicamente valores entre 0 y 1.

## Correlación entre los Datos

### Correlaciones con Todos los Datos


```python
corr = players.corr()
corr
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>goals</th>
      <th>assists</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_made</th>
      <th>pens_att</th>
      <th>...</th>
      <th>goals_per90</th>
      <th>assists_per90</th>
      <th>goals_assists_per90</th>
      <th>goals_pens_per90</th>
      <th>goals_assists_pens_per90</th>
      <th>xg_per90</th>
      <th>xg_assist_per90</th>
      <th>xg_xg_assist_per90</th>
      <th>npxg_per90</th>
      <th>npxg_xg_assist_per90</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>games</th>
      <td>1.000000</td>
      <td>0.920590</td>
      <td>0.935522</td>
      <td>0.935531</td>
      <td>0.445874</td>
      <td>0.495337</td>
      <td>0.522062</td>
      <td>0.451317</td>
      <td>0.218255</td>
      <td>0.233113</td>
      <td>...</td>
      <td>0.071405</td>
      <td>0.031262</td>
      <td>0.073672</td>
      <td>0.060716</td>
      <td>0.065508</td>
      <td>0.013241</td>
      <td>0.016941</td>
      <td>0.018942</td>
      <td>0.003604</td>
      <td>0.010854</td>
    </tr>
    <tr>
      <th>games_starts</th>
      <td>0.920590</td>
      <td>1.000000</td>
      <td>0.995269</td>
      <td>0.995264</td>
      <td>0.402000</td>
      <td>0.460770</td>
      <td>0.476639</td>
      <td>0.401546</td>
      <td>0.218602</td>
      <td>0.231430</td>
      <td>...</td>
      <td>0.026812</td>
      <td>0.004591</td>
      <td>0.023263</td>
      <td>0.017234</td>
      <td>0.015899</td>
      <td>-0.028880</td>
      <td>-0.021626</td>
      <td>-0.034206</td>
      <td>-0.037000</td>
      <td>-0.041219</td>
    </tr>
    <tr>
      <th>minutes</th>
      <td>0.935522</td>
      <td>0.995269</td>
      <td>1.000000</td>
      <td>0.999997</td>
      <td>0.399455</td>
      <td>0.456504</td>
      <td>0.473056</td>
      <td>0.399283</td>
      <td>0.216085</td>
      <td>0.229124</td>
      <td>...</td>
      <td>0.028110</td>
      <td>0.004461</td>
      <td>0.024171</td>
      <td>0.018641</td>
      <td>0.016889</td>
      <td>-0.027739</td>
      <td>-0.022053</td>
      <td>-0.033431</td>
      <td>-0.035837</td>
      <td>-0.040426</td>
    </tr>
    <tr>
      <th>minutes_90s</th>
      <td>0.935531</td>
      <td>0.995264</td>
      <td>0.999997</td>
      <td>1.000000</td>
      <td>0.399447</td>
      <td>0.456497</td>
      <td>0.473047</td>
      <td>0.399279</td>
      <td>0.216064</td>
      <td>0.229094</td>
      <td>...</td>
      <td>0.028082</td>
      <td>0.004493</td>
      <td>0.024169</td>
      <td>0.018613</td>
      <td>0.016888</td>
      <td>-0.027759</td>
      <td>-0.022027</td>
      <td>-0.033437</td>
      <td>-0.035857</td>
      <td>-0.040431</td>
    </tr>
    <tr>
      <th>goals</th>
      <td>0.445874</td>
      <td>0.402000</td>
      <td>0.399455</td>
      <td>0.399447</td>
      <td>1.000000</td>
      <td>0.553449</td>
      <td>0.936935</td>
      <td>0.981098</td>
      <td>0.616127</td>
      <td>0.636815</td>
      <td>...</td>
      <td>0.329496</td>
      <td>0.094855</td>
      <td>0.309347</td>
      <td>0.291596</td>
      <td>0.280083</td>
      <td>0.192533</td>
      <td>0.101297</td>
      <td>0.209233</td>
      <td>0.160771</td>
      <td>0.182734</td>
    </tr>
    <tr>
      <th>assists</th>
      <td>0.495337</td>
      <td>0.460770</td>
      <td>0.456504</td>
      <td>0.456497</td>
      <td>0.553449</td>
      <td>1.000000</td>
      <td>0.809642</td>
      <td>0.550371</td>
      <td>0.310941</td>
      <td>0.328064</td>
      <td>...</td>
      <td>0.139714</td>
      <td>0.256257</td>
      <td>0.264396</td>
      <td>0.122057</td>
      <td>0.252204</td>
      <td>0.081009</td>
      <td>0.187317</td>
      <td>0.153413</td>
      <td>0.065879</td>
      <td>0.141674</td>
    </tr>
    <tr>
      <th>goals_assists</th>
      <td>0.522062</td>
      <td>0.476639</td>
      <td>0.473056</td>
      <td>0.473047</td>
      <td>0.936935</td>
      <td>0.809642</td>
      <td>1.000000</td>
      <td>0.922323</td>
      <td>0.564659</td>
      <td>0.586424</td>
      <td>...</td>
      <td>0.290821</td>
      <td>0.174377</td>
      <td>0.328942</td>
      <td>0.256704</td>
      <td>0.303205</td>
      <td>0.169670</td>
      <td>0.149987</td>
      <td>0.211821</td>
      <td>0.140939</td>
      <td>0.188222</td>
    </tr>
    <tr>
      <th>goals_pens</th>
      <td>0.451317</td>
      <td>0.401546</td>
      <td>0.399283</td>
      <td>0.399279</td>
      <td>0.981098</td>
      <td>0.550371</td>
      <td>0.922323</td>
      <td>1.000000</td>
      <td>0.452061</td>
      <td>0.483992</td>
      <td>...</td>
      <td>0.328561</td>
      <td>0.094821</td>
      <td>0.308610</td>
      <td>0.304018</td>
      <td>0.289489</td>
      <td>0.185105</td>
      <td>0.098660</td>
      <td>0.201721</td>
      <td>0.163531</td>
      <td>0.183874</td>
    </tr>
    <tr>
      <th>pens_made</th>
      <td>0.218255</td>
      <td>0.218602</td>
      <td>0.216085</td>
      <td>0.216064</td>
      <td>0.616127</td>
      <td>0.310941</td>
      <td>0.564659</td>
      <td>0.452061</td>
      <td>1.000000</td>
      <td>0.965396</td>
      <td>...</td>
      <td>0.181463</td>
      <td>0.051285</td>
      <td>0.169796</td>
      <td>0.106663</td>
      <td>0.112736</td>
      <td>0.134046</td>
      <td>0.065351</td>
      <td>0.143393</td>
      <td>0.075452</td>
      <td>0.093889</td>
    </tr>
    <tr>
      <th>pens_att</th>
      <td>0.233113</td>
      <td>0.231430</td>
      <td>0.229124</td>
      <td>0.229094</td>
      <td>0.636815</td>
      <td>0.328064</td>
      <td>0.586424</td>
      <td>0.483992</td>
      <td>0.965396</td>
      <td>1.000000</td>
      <td>...</td>
      <td>0.186651</td>
      <td>0.053971</td>
      <td>0.175388</td>
      <td>0.115513</td>
      <td>0.121107</td>
      <td>0.141727</td>
      <td>0.067863</td>
      <td>0.151026</td>
      <td>0.080281</td>
      <td>0.099123</td>
    </tr>
    <tr>
      <th>cards_yellow</th>
      <td>0.609855</td>
      <td>0.627752</td>
      <td>0.626159</td>
      <td>0.626152</td>
      <td>0.198977</td>
      <td>0.264034</td>
      <td>0.251014</td>
      <td>0.197821</td>
      <td>0.111990</td>
      <td>0.120049</td>
      <td>...</td>
      <td>-0.003537</td>
      <td>-0.007928</td>
      <td>-0.007552</td>
      <td>-0.008328</td>
      <td>-0.011263</td>
      <td>-0.037844</td>
      <td>-0.030497</td>
      <td>-0.045866</td>
      <td>-0.042112</td>
      <td>-0.049651</td>
    </tr>
    <tr>
      <th>cards_red</th>
      <td>0.170323</td>
      <td>0.190493</td>
      <td>0.183566</td>
      <td>0.183566</td>
      <td>0.035882</td>
      <td>0.045906</td>
      <td>0.044549</td>
      <td>0.035626</td>
      <td>0.020386</td>
      <td>0.021321</td>
      <td>...</td>
      <td>-0.007526</td>
      <td>-0.011249</td>
      <td>-0.012707</td>
      <td>-0.008632</td>
      <td>-0.013627</td>
      <td>-0.024273</td>
      <td>-0.026824</td>
      <td>-0.032651</td>
      <td>-0.025088</td>
      <td>-0.033513</td>
    </tr>
    <tr>
      <th>xg</th>
      <td>0.406053</td>
      <td>0.351139</td>
      <td>0.349593</td>
      <td>0.349580</td>
      <td>0.768230</td>
      <td>0.469731</td>
      <td>0.738478</td>
      <td>0.735382</td>
      <td>0.547923</td>
      <td>0.571785</td>
      <td>...</td>
      <td>0.242654</td>
      <td>0.080430</td>
      <td>0.234341</td>
      <td>0.207646</td>
      <td>0.207466</td>
      <td>0.283358</td>
      <td>0.173078</td>
      <td>0.318785</td>
      <td>0.243328</td>
      <td>0.285659</td>
    </tr>
    <tr>
      <th>npxg</th>
      <td>0.416240</td>
      <td>0.353575</td>
      <td>0.352303</td>
      <td>0.352294</td>
      <td>0.745951</td>
      <td>0.468274</td>
      <td>0.722167</td>
      <td>0.744835</td>
      <td>0.406751</td>
      <td>0.427352</td>
      <td>...</td>
      <td>0.238305</td>
      <td>0.080605</td>
      <td>0.231128</td>
      <td>0.214566</td>
      <td>0.212835</td>
      <td>0.281633</td>
      <td>0.174586</td>
      <td>0.317992</td>
      <td>0.253559</td>
      <td>0.295042</td>
    </tr>
    <tr>
      <th>xg_assist</th>
      <td>0.468071</td>
      <td>0.425871</td>
      <td>0.421864</td>
      <td>0.421861</td>
      <td>0.493190</td>
      <td>0.714781</td>
      <td>0.647491</td>
      <td>0.482377</td>
      <td>0.309933</td>
      <td>0.323807</td>
      <td>...</td>
      <td>0.124266</td>
      <td>0.150471</td>
      <td>0.187399</td>
      <td>0.106210</td>
      <td>0.174252</td>
      <td>0.148981</td>
      <td>0.303915</td>
      <td>0.263794</td>
      <td>0.127142</td>
      <td>0.246971</td>
    </tr>
    <tr>
      <th>npxg_xg_assist</th>
      <td>0.478250</td>
      <td>0.418887</td>
      <td>0.416257</td>
      <td>0.416250</td>
      <td>0.702715</td>
      <td>0.622125</td>
      <td>0.756259</td>
      <td>0.697182</td>
      <td>0.401416</td>
      <td>0.420923</td>
      <td>...</td>
      <td>0.209624</td>
      <td>0.119317</td>
      <td>0.233168</td>
      <td>0.186213</td>
      <td>0.215470</td>
      <td>0.248694</td>
      <td>0.248621</td>
      <td>0.323474</td>
      <td>0.220790</td>
      <td>0.301122</td>
    </tr>
    <tr>
      <th>progressive_carries</th>
      <td>0.485366</td>
      <td>0.444934</td>
      <td>0.443012</td>
      <td>0.442996</td>
      <td>0.402541</td>
      <td>0.551402</td>
      <td>0.515052</td>
      <td>0.402921</td>
      <td>0.215496</td>
      <td>0.227331</td>
      <td>...</td>
      <td>0.089078</td>
      <td>0.092555</td>
      <td>0.124863</td>
      <td>0.077755</td>
      <td>0.116564</td>
      <td>0.115860</td>
      <td>0.211307</td>
      <td>0.193876</td>
      <td>0.100924</td>
      <td>0.182335</td>
    </tr>
    <tr>
      <th>progressive_passes</th>
      <td>0.541614</td>
      <td>0.553840</td>
      <td>0.550478</td>
      <td>0.550463</td>
      <td>0.237213</td>
      <td>0.430110</td>
      <td>0.347649</td>
      <td>0.228811</td>
      <td>0.162101</td>
      <td>0.167697</td>
      <td>...</td>
      <td>0.015646</td>
      <td>0.044871</td>
      <td>0.039567</td>
      <td>0.007708</td>
      <td>0.033750</td>
      <td>0.039313</td>
      <td>0.137434</td>
      <td>0.095546</td>
      <td>0.027985</td>
      <td>0.086709</td>
    </tr>
    <tr>
      <th>goals_per90</th>
      <td>0.071405</td>
      <td>0.026812</td>
      <td>0.028110</td>
      <td>0.028082</td>
      <td>0.329496</td>
      <td>0.139714</td>
      <td>0.290821</td>
      <td>0.328561</td>
      <td>0.181463</td>
      <td>0.186651</td>
      <td>...</td>
      <td>1.000000</td>
      <td>0.042984</td>
      <td>0.787752</td>
      <td>0.993438</td>
      <td>0.779805</td>
      <td>0.752357</td>
      <td>0.048725</td>
      <td>0.660913</td>
      <td>0.745696</td>
      <td>0.654836</td>
    </tr>
    <tr>
      <th>assists_per90</th>
      <td>0.031262</td>
      <td>0.004591</td>
      <td>0.004461</td>
      <td>0.004493</td>
      <td>0.094855</td>
      <td>0.256257</td>
      <td>0.174377</td>
      <td>0.094821</td>
      <td>0.051285</td>
      <td>0.053971</td>
      <td>...</td>
      <td>0.042984</td>
      <td>1.000000</td>
      <td>0.649257</td>
      <td>0.039196</td>
      <td>0.652916</td>
      <td>0.028587</td>
      <td>0.481326</td>
      <td>0.241699</td>
      <td>0.025455</td>
      <td>0.241970</td>
    </tr>
    <tr>
      <th>goals_assists_per90</th>
      <td>0.073672</td>
      <td>0.023263</td>
      <td>0.024171</td>
      <td>0.024169</td>
      <td>0.309347</td>
      <td>0.264396</td>
      <td>0.328942</td>
      <td>0.308610</td>
      <td>0.169796</td>
      <td>0.175388</td>
      <td>...</td>
      <td>0.787752</td>
      <td>0.649257</td>
      <td>1.000000</td>
      <td>0.780421</td>
      <td>0.996202</td>
      <td>0.590365</td>
      <td>0.333849</td>
      <td>0.652143</td>
      <td>0.583362</td>
      <td>0.647683</td>
    </tr>
    <tr>
      <th>goals_pens_per90</th>
      <td>0.060716</td>
      <td>0.017234</td>
      <td>0.018641</td>
      <td>0.018613</td>
      <td>0.291596</td>
      <td>0.122057</td>
      <td>0.256704</td>
      <td>0.304018</td>
      <td>0.106663</td>
      <td>0.115513</td>
      <td>...</td>
      <td>0.993438</td>
      <td>0.039196</td>
      <td>0.780421</td>
      <td>1.000000</td>
      <td>0.782418</td>
      <td>0.746955</td>
      <td>0.044111</td>
      <td>0.654240</td>
      <td>0.750364</td>
      <td>0.656684</td>
    </tr>
    <tr>
      <th>goals_assists_pens_per90</th>
      <td>0.065508</td>
      <td>0.015899</td>
      <td>0.016889</td>
      <td>0.016888</td>
      <td>0.280083</td>
      <td>0.252204</td>
      <td>0.303205</td>
      <td>0.289489</td>
      <td>0.112736</td>
      <td>0.121107</td>
      <td>...</td>
      <td>0.779805</td>
      <td>0.652916</td>
      <td>0.996202</td>
      <td>0.782418</td>
      <td>1.000000</td>
      <td>0.584011</td>
      <td>0.333401</td>
      <td>0.646545</td>
      <td>0.584646</td>
      <td>0.648569</td>
    </tr>
    <tr>
      <th>xg_per90</th>
      <td>0.013241</td>
      <td>-0.028880</td>
      <td>-0.027739</td>
      <td>-0.027759</td>
      <td>0.192533</td>
      <td>0.081009</td>
      <td>0.169670</td>
      <td>0.185105</td>
      <td>0.134046</td>
      <td>0.141727</td>
      <td>...</td>
      <td>0.752357</td>
      <td>0.028587</td>
      <td>0.590365</td>
      <td>0.746955</td>
      <td>0.584011</td>
      <td>1.000000</td>
      <td>0.097548</td>
      <td>0.893232</td>
      <td>0.994496</td>
      <td>0.888210</td>
    </tr>
    <tr>
      <th>xg_assist_per90</th>
      <td>0.016941</td>
      <td>-0.021626</td>
      <td>-0.022053</td>
      <td>-0.022027</td>
      <td>0.101297</td>
      <td>0.187317</td>
      <td>0.149987</td>
      <td>0.098660</td>
      <td>0.065351</td>
      <td>0.067863</td>
      <td>...</td>
      <td>0.048725</td>
      <td>0.481326</td>
      <td>0.333849</td>
      <td>0.044111</td>
      <td>0.333401</td>
      <td>0.097548</td>
      <td>1.000000</td>
      <td>0.534499</td>
      <td>0.091291</td>
      <td>0.535199</td>
    </tr>
    <tr>
      <th>xg_xg_assist_per90</th>
      <td>0.018942</td>
      <td>-0.034206</td>
      <td>-0.033431</td>
      <td>-0.033437</td>
      <td>0.209233</td>
      <td>0.153413</td>
      <td>0.211821</td>
      <td>0.201721</td>
      <td>0.143393</td>
      <td>0.151026</td>
      <td>...</td>
      <td>0.660913</td>
      <td>0.241699</td>
      <td>0.652143</td>
      <td>0.654240</td>
      <td>0.646545</td>
      <td>0.893232</td>
      <td>0.534499</td>
      <td>1.000000</td>
      <td>0.885736</td>
      <td>0.996050</td>
    </tr>
    <tr>
      <th>npxg_per90</th>
      <td>0.003604</td>
      <td>-0.037000</td>
      <td>-0.035837</td>
      <td>-0.035857</td>
      <td>0.160771</td>
      <td>0.065879</td>
      <td>0.140939</td>
      <td>0.163531</td>
      <td>0.075452</td>
      <td>0.080281</td>
      <td>...</td>
      <td>0.745696</td>
      <td>0.025455</td>
      <td>0.583362</td>
      <td>0.750364</td>
      <td>0.584646</td>
      <td>0.994496</td>
      <td>0.091291</td>
      <td>0.885736</td>
      <td>1.000000</td>
      <td>0.890010</td>
    </tr>
    <tr>
      <th>npxg_xg_assist_per90</th>
      <td>0.010854</td>
      <td>-0.041219</td>
      <td>-0.040426</td>
      <td>-0.040431</td>
      <td>0.182734</td>
      <td>0.141674</td>
      <td>0.188222</td>
      <td>0.183874</td>
      <td>0.093889</td>
      <td>0.099123</td>
      <td>...</td>
      <td>0.654836</td>
      <td>0.241970</td>
      <td>0.647683</td>
      <td>0.656684</td>
      <td>0.648569</td>
      <td>0.888210</td>
      <td>0.535199</td>
      <td>0.996050</td>
      <td>0.890010</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>
<p>28 rows × 28 columns</p>





```python
corr['xg'].sort_values(ascending=False)
```




    xg                          1.000000
    npxg                        0.980614
    npxg_xg_assist              0.930104
    goals                       0.768230
    goals_assists               0.738478
    goals_pens                  0.735382
    xg_assist                   0.662501
    pens_att                    0.571785
    progressive_carries         0.570685
    pens_made                   0.547923
    assists                     0.469731
    games                       0.406053
    progressive_passes          0.387461
    games_starts                0.351139
    minutes                     0.349593
    minutes_90s                 0.349580
    xg_xg_assist_per90          0.318785
    npxg_xg_assist_per90        0.285659
    xg_per90                    0.283358
    npxg_per90                  0.243328
    goals_per90                 0.242654
    goals_assists_per90         0.234341
    goals_pens_per90            0.207646
    goals_assists_pens_per90    0.207466
    cards_yellow                0.174997
    xg_assist_per90             0.173078
    assists_per90               0.080430
    cards_red                   0.016007
    Name: xg, dtype: float64




```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

mask = np.triu(np.ones_like(corr, dtype=bool))

plt.figure(figsize=(12, 8))
sns.heatmap(corr, mask=mask, fmt='.2f', square=True)
plt.show()
```


    
![corr](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_85_0.png)
    


Vemos que las estadísticas avanzadas tienen mucha correlación con los xG ya que dependen de ellos. Como no las vamos a necesitar, vamos a comprobar la correlación de los datos sin ellas.

### Correlaciones sin Estadística Avanzada


```python
players_wo_x = players[["player", "season", "team", "goals", "goals_pens", "goals_assists", "pens_att", "pens_made", "assists", "progressive_carries", "games", "games_starts", "minutes", "minutes_90s", "progressive_passes", "goals_assists_per90", "goals_per90", "cards_yellow", "goals_assists_pens_per90", "goals_pens_per90", "assists_per90", "cards_red", "xg"]]
players_wo_x
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>player</th>
      <th>season</th>
      <th>team</th>
      <th>goals</th>
      <th>goals_pens</th>
      <th>goals_assists</th>
      <th>pens_att</th>
      <th>pens_made</th>
      <th>assists</th>
      <th>progressive_carries</th>
      <th>...</th>
      <th>minutes_90s</th>
      <th>progressive_passes</th>
      <th>goals_assists_per90</th>
      <th>goals_per90</th>
      <th>cards_yellow</th>
      <th>goals_assists_pens_per90</th>
      <th>goals_pens_per90</th>
      <th>assists_per90</th>
      <th>cards_red</th>
      <th>xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>David Abraham</td>
      <td>2015-2016</td>
      <td>Eint Frankfurt</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>28.3</td>
      <td>0</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>8</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>René Adler</td>
      <td>2015-2016</td>
      <td>Hamburger SV</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>...</td>
      <td>23.0</td>
      <td>0</td>
      <td>0.04</td>
      <td>0.00</td>
      <td>3</td>
      <td>0.04</td>
      <td>0.00</td>
      <td>0.04</td>
      <td>1</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Stefan Aigner</td>
      <td>2015-2016</td>
      <td>Eint Frankfurt</td>
      <td>3</td>
      <td>3</td>
      <td>6</td>
      <td>0</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>...</td>
      <td>26.6</td>
      <td>0</td>
      <td>0.23</td>
      <td>0.11</td>
      <td>7</td>
      <td>0.23</td>
      <td>0.11</td>
      <td>0.11</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Albian Ajeti</td>
      <td>2015-2016</td>
      <td>Augsburg</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>0.4</td>
      <td>0</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>David Alaba</td>
      <td>2015-2016</td>
      <td>Bayern Munich</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>27.7</td>
      <td>0</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>2</td>
      <td>0.07</td>
      <td>0.07</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>23705</th>
      <td>Nadir Zortea</td>
      <td>2023-2024</td>
      <td>Atalanta</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>7</td>
      <td>...</td>
      <td>1.7</td>
      <td>10</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>1</td>
      <td>0.60</td>
      <td>0.60</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>23706</th>
      <td>Szymon Żurkowski</td>
      <td>2023-2024</td>
      <td>Empoli</td>
      <td>4</td>
      <td>4</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>9</td>
      <td>...</td>
      <td>3.2</td>
      <td>10</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>1</td>
      <td>1.27</td>
      <td>1.27</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.5</td>
    </tr>
    <tr>
      <th>23707</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Hellas Verona</td>
      <td>5</td>
      <td>4</td>
      <td>6</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>3</td>
      <td>...</td>
      <td>13.4</td>
      <td>15</td>
      <td>0.45</td>
      <td>0.37</td>
      <td>2</td>
      <td>0.37</td>
      <td>0.30</td>
      <td>0.07</td>
      <td>0</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>23708</th>
      <td>Milan Đurić</td>
      <td>2023-2024</td>
      <td>Monza</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>...</td>
      <td>1.4</td>
      <td>1</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>23709</th>
      <td>Mateusz Łęgowski</td>
      <td>2023-2024</td>
      <td>Salernitana</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>14</td>
      <td>...</td>
      <td>9.8</td>
      <td>33</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>3</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0.00</td>
      <td>0</td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
<p>23710 rows × 23 columns</p>




```python
corr = players_wo_x.corr()
corr
```




<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>goals</th>
      <th>goals_pens</th>
      <th>goals_assists</th>
      <th>pens_att</th>
      <th>pens_made</th>
      <th>assists</th>
      <th>progressive_carries</th>
      <th>games</th>
      <th>games_starts</th>
      <th>minutes</th>
      <th>minutes_90s</th>
      <th>progressive_passes</th>
      <th>goals_assists_per90</th>
      <th>goals_per90</th>
      <th>cards_yellow</th>
      <th>goals_assists_pens_per90</th>
      <th>goals_pens_per90</th>
      <th>assists_per90</th>
      <th>cards_red</th>
      <th>xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>goals</th>
      <td>1.000000</td>
      <td>0.981098</td>
      <td>0.936935</td>
      <td>0.636815</td>
      <td>0.616127</td>
      <td>0.553449</td>
      <td>0.402541</td>
      <td>0.445874</td>
      <td>0.402000</td>
      <td>0.399455</td>
      <td>0.399447</td>
      <td>0.237213</td>
      <td>0.309347</td>
      <td>0.329496</td>
      <td>0.198977</td>
      <td>0.280083</td>
      <td>0.291596</td>
      <td>0.094855</td>
      <td>0.035882</td>
      <td>0.768230</td>
    </tr>
    <tr>
      <th>goals_pens</th>
      <td>0.981098</td>
      <td>1.000000</td>
      <td>0.922323</td>
      <td>0.483992</td>
      <td>0.452061</td>
      <td>0.550371</td>
      <td>0.402921</td>
      <td>0.451317</td>
      <td>0.401546</td>
      <td>0.399283</td>
      <td>0.399279</td>
      <td>0.228811</td>
      <td>0.308610</td>
      <td>0.328561</td>
      <td>0.197821</td>
      <td>0.289489</td>
      <td>0.304018</td>
      <td>0.094821</td>
      <td>0.035626</td>
      <td>0.735382</td>
    </tr>
    <tr>
      <th>goals_assists</th>
      <td>0.936935</td>
      <td>0.922323</td>
      <td>1.000000</td>
      <td>0.586424</td>
      <td>0.564659</td>
      <td>0.809642</td>
      <td>0.515052</td>
      <td>0.522062</td>
      <td>0.476639</td>
      <td>0.473056</td>
      <td>0.473047</td>
      <td>0.347649</td>
      <td>0.328942</td>
      <td>0.290821</td>
      <td>0.251014</td>
      <td>0.303205</td>
      <td>0.256704</td>
      <td>0.174377</td>
      <td>0.044549</td>
      <td>0.738478</td>
    </tr>
    <tr>
      <th>pens_att</th>
      <td>0.636815</td>
      <td>0.483992</td>
      <td>0.586424</td>
      <td>1.000000</td>
      <td>0.965396</td>
      <td>0.328064</td>
      <td>0.227331</td>
      <td>0.233113</td>
      <td>0.231430</td>
      <td>0.229124</td>
      <td>0.229094</td>
      <td>0.167697</td>
      <td>0.175388</td>
      <td>0.186651</td>
      <td>0.120049</td>
      <td>0.121107</td>
      <td>0.115513</td>
      <td>0.053971</td>
      <td>0.021321</td>
      <td>0.571785</td>
    </tr>
    <tr>
      <th>pens_made</th>
      <td>0.616127</td>
      <td>0.452061</td>
      <td>0.564659</td>
      <td>0.965396</td>
      <td>1.000000</td>
      <td>0.310941</td>
      <td>0.215496</td>
      <td>0.218255</td>
      <td>0.218602</td>
      <td>0.216085</td>
      <td>0.216064</td>
      <td>0.162101</td>
      <td>0.169796</td>
      <td>0.181463</td>
      <td>0.111990</td>
      <td>0.112736</td>
      <td>0.106663</td>
      <td>0.051285</td>
      <td>0.020386</td>
      <td>0.547923</td>
    </tr>
    <tr>
      <th>assists</th>
      <td>0.553449</td>
      <td>0.550371</td>
      <td>0.809642</td>
      <td>0.328064</td>
      <td>0.310941</td>
      <td>1.000000</td>
      <td>0.551402</td>
      <td>0.495337</td>
      <td>0.460770</td>
      <td>0.456504</td>
      <td>0.456497</td>
      <td>0.430110</td>
      <td>0.264396</td>
      <td>0.139714</td>
      <td>0.264034</td>
      <td>0.252204</td>
      <td>0.122057</td>
      <td>0.256257</td>
      <td>0.045906</td>
      <td>0.469731</td>
    </tr>
    <tr>
      <th>progressive_carries</th>
      <td>0.402541</td>
      <td>0.402921</td>
      <td>0.515052</td>
      <td>0.227331</td>
      <td>0.215496</td>
      <td>0.551402</td>
      <td>1.000000</td>
      <td>0.485366</td>
      <td>0.444934</td>
      <td>0.443012</td>
      <td>0.442996</td>
      <td>0.689643</td>
      <td>0.124863</td>
      <td>0.089078</td>
      <td>0.268624</td>
      <td>0.116564</td>
      <td>0.077755</td>
      <td>0.092555</td>
      <td>0.043844</td>
      <td>0.570685</td>
    </tr>
    <tr>
      <th>games</th>
      <td>0.445874</td>
      <td>0.451317</td>
      <td>0.522062</td>
      <td>0.233113</td>
      <td>0.218255</td>
      <td>0.495337</td>
      <td>0.485366</td>
      <td>1.000000</td>
      <td>0.920590</td>
      <td>0.935522</td>
      <td>0.935531</td>
      <td>0.541614</td>
      <td>0.073672</td>
      <td>0.071405</td>
      <td>0.609855</td>
      <td>0.065508</td>
      <td>0.060716</td>
      <td>0.031262</td>
      <td>0.170323</td>
      <td>0.406053</td>
    </tr>
    <tr>
      <th>games_starts</th>
      <td>0.402000</td>
      <td>0.401546</td>
      <td>0.476639</td>
      <td>0.231430</td>
      <td>0.218602</td>
      <td>0.460770</td>
      <td>0.444934</td>
      <td>0.920590</td>
      <td>1.000000</td>
      <td>0.995269</td>
      <td>0.995264</td>
      <td>0.553840</td>
      <td>0.023263</td>
      <td>0.026812</td>
      <td>0.627752</td>
      <td>0.015899</td>
      <td>0.017234</td>
      <td>0.004591</td>
      <td>0.190493</td>
      <td>0.351139</td>
    </tr>
    <tr>
      <th>minutes</th>
      <td>0.399455</td>
      <td>0.399283</td>
      <td>0.473056</td>
      <td>0.229124</td>
      <td>0.216085</td>
      <td>0.456504</td>
      <td>0.443012</td>
      <td>0.935522</td>
      <td>0.995269</td>
      <td>1.000000</td>
      <td>0.999997</td>
      <td>0.550478</td>
      <td>0.024171</td>
      <td>0.028110</td>
      <td>0.626159</td>
      <td>0.016889</td>
      <td>0.018641</td>
      <td>0.004461</td>
      <td>0.183566</td>
      <td>0.349593</td>
    </tr>
    <tr>
      <th>minutes_90s</th>
      <td>0.399447</td>
      <td>0.399279</td>
      <td>0.473047</td>
      <td>0.229094</td>
      <td>0.216064</td>
      <td>0.456497</td>
      <td>0.442996</td>
      <td>0.935531</td>
      <td>0.995264</td>
      <td>0.999997</td>
      <td>1.000000</td>
      <td>0.550463</td>
      <td>0.024169</td>
      <td>0.028082</td>
      <td>0.626152</td>
      <td>0.016888</td>
      <td>0.018613</td>
      <td>0.004493</td>
      <td>0.183566</td>
      <td>0.349580</td>
    </tr>
    <tr>
      <th>progressive_passes</th>
      <td>0.237213</td>
      <td>0.228811</td>
      <td>0.347649</td>
      <td>0.167697</td>
      <td>0.162101</td>
      <td>0.430110</td>
      <td>0.689643</td>
      <td>0.541614</td>
      <td>0.553840</td>
      <td>0.550478</td>
      <td>0.550463</td>
      <td>1.000000</td>
      <td>0.039567</td>
      <td>0.015646</td>
      <td>0.450221</td>
      <td>0.033750</td>
      <td>0.007708</td>
      <td>0.044871</td>
      <td>0.105611</td>
      <td>0.387461</td>
    </tr>
    <tr>
      <th>goals_assists_per90</th>
      <td>0.309347</td>
      <td>0.308610</td>
      <td>0.328942</td>
      <td>0.175388</td>
      <td>0.169796</td>
      <td>0.264396</td>
      <td>0.124863</td>
      <td>0.073672</td>
      <td>0.023263</td>
      <td>0.024171</td>
      <td>0.024169</td>
      <td>0.039567</td>
      <td>1.000000</td>
      <td>0.787752</td>
      <td>-0.007552</td>
      <td>0.996202</td>
      <td>0.780421</td>
      <td>0.649257</td>
      <td>-0.012707</td>
      <td>0.234341</td>
    </tr>
    <tr>
      <th>goals_per90</th>
      <td>0.329496</td>
      <td>0.328561</td>
      <td>0.290821</td>
      <td>0.186651</td>
      <td>0.181463</td>
      <td>0.139714</td>
      <td>0.089078</td>
      <td>0.071405</td>
      <td>0.026812</td>
      <td>0.028110</td>
      <td>0.028082</td>
      <td>0.015646</td>
      <td>0.787752</td>
      <td>1.000000</td>
      <td>-0.003537</td>
      <td>0.779805</td>
      <td>0.993438</td>
      <td>0.042984</td>
      <td>-0.007526</td>
      <td>0.242654</td>
    </tr>
    <tr>
      <th>cards_yellow</th>
      <td>0.198977</td>
      <td>0.197821</td>
      <td>0.251014</td>
      <td>0.120049</td>
      <td>0.111990</td>
      <td>0.264034</td>
      <td>0.268624</td>
      <td>0.609855</td>
      <td>0.627752</td>
      <td>0.626159</td>
      <td>0.626152</td>
      <td>0.450221</td>
      <td>-0.007552</td>
      <td>-0.003537</td>
      <td>1.000000</td>
      <td>-0.011263</td>
      <td>-0.008328</td>
      <td>-0.007928</td>
      <td>0.292797</td>
      <td>0.174997</td>
    </tr>
    <tr>
      <th>goals_assists_pens_per90</th>
      <td>0.280083</td>
      <td>0.289489</td>
      <td>0.303205</td>
      <td>0.121107</td>
      <td>0.112736</td>
      <td>0.252204</td>
      <td>0.116564</td>
      <td>0.065508</td>
      <td>0.015899</td>
      <td>0.016889</td>
      <td>0.016888</td>
      <td>0.033750</td>
      <td>0.996202</td>
      <td>0.779805</td>
      <td>-0.011263</td>
      <td>1.000000</td>
      <td>0.782418</td>
      <td>0.652916</td>
      <td>-0.013627</td>
      <td>0.207466</td>
    </tr>
    <tr>
      <th>goals_pens_per90</th>
      <td>0.291596</td>
      <td>0.304018</td>
      <td>0.256704</td>
      <td>0.115513</td>
      <td>0.106663</td>
      <td>0.122057</td>
      <td>0.077755</td>
      <td>0.060716</td>
      <td>0.017234</td>
      <td>0.018641</td>
      <td>0.018613</td>
      <td>0.007708</td>
      <td>0.780421</td>
      <td>0.993438</td>
      <td>-0.008328</td>
      <td>0.782418</td>
      <td>1.000000</td>
      <td>0.039196</td>
      <td>-0.008632</td>
      <td>0.207646</td>
    </tr>
    <tr>
      <th>assists_per90</th>
      <td>0.094855</td>
      <td>0.094821</td>
      <td>0.174377</td>
      <td>0.053971</td>
      <td>0.051285</td>
      <td>0.256257</td>
      <td>0.092555</td>
      <td>0.031262</td>
      <td>0.004591</td>
      <td>0.004461</td>
      <td>0.004493</td>
      <td>0.044871</td>
      <td>0.649257</td>
      <td>0.042984</td>
      <td>-0.007928</td>
      <td>0.652916</td>
      <td>0.039196</td>
      <td>1.000000</td>
      <td>-0.011249</td>
      <td>0.080430</td>
    </tr>
    <tr>
      <th>cards_red</th>
      <td>0.035882</td>
      <td>0.035626</td>
      <td>0.044549</td>
      <td>0.021321</td>
      <td>0.020386</td>
      <td>0.045906</td>
      <td>0.043844</td>
      <td>0.170323</td>
      <td>0.190493</td>
      <td>0.183566</td>
      <td>0.183566</td>
      <td>0.105611</td>
      <td>-0.012707</td>
      <td>-0.007526</td>
      <td>0.292797</td>
      <td>-0.013627</td>
      <td>-0.008632</td>
      <td>-0.011249</td>
      <td>1.000000</td>
      <td>0.016007</td>
    </tr>
    <tr>
      <th>xg</th>
      <td>0.768230</td>
      <td>0.735382</td>
      <td>0.738478</td>
      <td>0.571785</td>
      <td>0.547923</td>
      <td>0.469731</td>
      <td>0.570685</td>
      <td>0.406053</td>
      <td>0.351139</td>
      <td>0.349593</td>
      <td>0.349580</td>
      <td>0.387461</td>
      <td>0.234341</td>
      <td>0.242654</td>
      <td>0.174997</td>
      <td>0.207466</td>
      <td>0.207646</td>
      <td>0.080430</td>
      <td>0.016007</td>
      <td>1.000000</td>
    </tr>
  </tbody>
</table>



```python
corr['xg'].sort_values(ascending=False)
```




    xg                          1.000000
    goals                       0.768230
    goals_assists               0.738478
    goals_pens                  0.735382
    pens_att                    0.571785
    progressive_carries         0.570685
    pens_made                   0.547923
    assists                     0.469731
    games                       0.406053
    progressive_passes          0.387461
    games_starts                0.351139
    minutes                     0.349593
    minutes_90s                 0.349580
    goals_per90                 0.242654
    goals_assists_per90         0.234341
    goals_pens_per90            0.207646
    goals_assists_pens_per90    0.207466
    cards_yellow                0.174997
    assists_per90               0.080430
    cards_red                   0.016007
    Name: xg, dtype: float64



Tomando esta correlación vamos a quedarnos con los 8 primeras columnas:

- `goals`: Los goles que acaba metiendo realmente el jugador.

- `goals_assists`: La suma de goles y asistencias.

- `goals_pens`: Los goles anotados que no han sido de penalti.

- `pens_att`: Los lanzamientos de penalti que ha realizado el jugador.

- `progressive_carries`: Los avances progresivos en los últimos 10 metros de campo que pueden acabar en gol.

- `pens_made`: Los lanzamientos de penalti anotados.

- `assists`: Las asistencias que ha realizado el jugador.

- `games`: Partidos que ha jugado el jugador en la temporada. Mientras más partidos juegue más ocasiones de gol puede generar.


```python
from pandas.plotting import scatter_matrix

attributes = ["games", "goals", "goals_assists", "goals_pens", "pens_att", "progressive_carries", "pens_made", "assists"]
scatter_matrix(players[attributes], figsize=(12,12))
plt.show()
```


    
![scatter_matrix](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_92_0.png)


Pese a haber cierta dispersión en los datos, podemos ver como se pueden apreciar líneas rectas que marcan la correlación.


## Limpieza de los Datos

Después de haber realizado un estudio de los datos vamos a quedarnos con los que nos han resultado realmente relevantes para el posterior entrenamiento:


### Cambios Realizados durante el Scrapping

- Cambio del formato de los minutos.

![minute_format_change](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/scrapping%20data%20transform/minutes.jpg)

<br>

- Transformación de datos de `object` a `float` o `int` respectivamente.

![data_type_change](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/scrapping%20data%20transform/data%20transform.jpg)

<br>

- Gestión de nulos: Pasamos los datos que nos llegan nulos a 0.

![null_management](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/scrapping%20data%20transform/nulls.jpg)


### Preparación de PySpark para Trabajar los Datos:

Para esta limpieza de datos vamos a usar PySpark. PySpark es una biblioteca de código abierto para análisis de datos distribuidos en el framework Apache Spark. Permite el procesamiento de grandes conjuntos de datos de manera distribuida en clústeres, utilizando el lenguaje de programación Python. PySpark facilita tareas como la manipulación, transformación y análisis de datos a gran escala, aprovechando la capacidad de procesamiento paralelo de Spark.


```python
!pip install -q findspark
!pip install pyspark
```

    Collecting pyspark
      Downloading pyspark-3.5.0.tar.gz (316.9 MB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m316.9/316.9 MB[0m [31m4.5 MB/s[0m eta [36m0:00:00[0m
    [?25h  Preparing metadata (setup.py) ... [?25l[?25hdone
    Requirement already satisfied: py4j==0.10.9.7 in /usr/local/lib/python3.10/dist-packages (from pyspark) (0.10.9.7)
    Building wheels for collected packages: pyspark
      Building wheel for pyspark (setup.py) ... [?25l[?25hdone
      Created wheel for pyspark: filename=pyspark-3.5.0-py2.py3-none-any.whl size=317425345 sha256=b245e19e43142534abf0fe81dc44cbae02914692513b9a79099668329de2de68
      Stored in directory: /root/.cache/pip/wheels/41/4e/10/c2cf2467f71c678cfc8a6b9ac9241e5e44a01940da8fbb17fc
    Successfully built pyspark
    Installing collected packages: pyspark
    Successfully installed pyspark-3.5.0



```python
import findspark
findspark.init()

import pyspark
from pyspark.sql import functions as f
```


```python
from pyspark.sql import SparkSession

spark = SparkSession.builder\
        .master("local[*]")\
        .appName('ExpectedFoot')\
        .getOrCreate()
```


```python
players_spark = spark.createDataFrame(players)
players_spark
```




    DataFrame[player: string, season: string, team: string, games: bigint, games_starts: bigint, minutes: bigint, minutes_90s: double, goals: bigint, assists: bigint, goals_assists: bigint, goals_pens: bigint, pens_made: bigint, pens_att: bigint, cards_yellow: bigint, cards_red: bigint, xg: double, npxg: double, xg_assist: double, npxg_xg_assist: double, progressive_carries: bigint, progressive_passes: bigint, goals_per90: double, assists_per90: double, goals_assists_per90: double, goals_pens_per90: double, goals_assists_pens_per90: double, xg_per90: double, xg_assist_per90: double, xg_xg_assist_per90: double, npxg_per90: double, npxg_xg_assist_per90: double]




```python
players_spark.show(5)
```

    +-------------+---------+--------------+-----+------------+-------+-----------+-----+-------+-------------+----------+---------+--------+------------+---------+---+----+---------+--------------+-------------------+------------------+-----------+-------------+-------------------+----------------+------------------------+--------+---------------+------------------+----------+--------------------+
    |       player|   season|          team|games|games_starts|minutes|minutes_90s|goals|assists|goals_assists|goals_pens|pens_made|pens_att|cards_yellow|cards_red| xg|npxg|xg_assist|npxg_xg_assist|progressive_carries|progressive_passes|goals_per90|assists_per90|goals_assists_per90|goals_pens_per90|goals_assists_pens_per90|xg_per90|xg_assist_per90|xg_xg_assist_per90|npxg_per90|npxg_xg_assist_per90|
    +-------------+---------+--------------+-----+------------+-------+-----------+-----+-------+-------------+----------+---------+--------+------------+---------+---+----+---------+--------------+-------------------+------------------+-----------+-------------+-------------------+----------------+------------------------+--------+---------------+------------------+----------+--------------------+
    |David Abraham|2015-2016|Eint Frankfurt|   31|          28|   2547|       28.3|    0|      0|            0|         0|        0|       0|           8|        0|0.0| 0.0|      0.0|           0.0|                  0|                 0|        0.0|          0.0|                0.0|             0.0|                     0.0|     0.0|            0.0|               0.0|       0.0|                 0.0|
    |   René Adler|2015-2016|  Hamburger SV|   24|          24|   2071|       23.0|    0|      1|            1|         0|        0|       0|           3|        1|0.0| 0.0|      0.0|           0.0|                  0|                 0|        0.0|         0.04|               0.04|             0.0|                    0.04|     0.0|            0.0|               0.0|       0.0|                 0.0|
    |Stefan Aigner|2015-2016|Eint Frankfurt|   31|          27|   2394|       26.6|    3|      3|            6|         3|        0|       0|           7|        0|0.0| 0.0|      0.0|           0.0|                  0|                 0|       0.11|         0.11|               0.23|            0.11|                    0.23|     0.0|            0.0|               0.0|       0.0|                 0.0|
    | Albian Ajeti|2015-2016|      Augsburg|    1|           0|     37|        0.4|    0|      0|            0|         0|        0|       0|           0|        0|0.0| 0.0|      0.0|           0.0|                  0|                 0|        0.0|          0.0|                0.0|             0.0|                     0.0|     0.0|            0.0|               0.0|       0.0|                 0.0|
    |  David Alaba|2015-2016| Bayern Munich|   30|          27|   2492|       27.7|    2|      0|            2|         2|        0|       0|           2|        0|0.0| 0.0|      0.0|           0.0|                  0|                 0|       0.07|          0.0|               0.07|            0.07|                    0.07|     0.0|            0.0|               0.0|       0.0|                 0.0|
    +-------------+---------+--------------+-----+------------+-------+-----------+-----+-------+-------------+----------+---------+--------+------------+---------+---+----+---------+--------------+-------------------+------------------+-----------+-------------+-------------------+----------------+------------------------+--------+---------------+------------------+----------+--------------------+
    only showing top 5 rows
    


### Eliminación de los Datos de las temporadas 2015/2016 y 2016/2017


```python
from pyspark.sql.functions import col

season_to_delete = ["2015-2016", "2016-2017"]

# Filtra el DataFrame para mantener solo las temporadas deseadas
players_spark = players_spark.filter(~col("season").isin(season_to_delete))

# Muestra el DataFrame resultante
players_spark.show()
```

    +------------------+---------+--------------+-----+------------+-------+-----------+-----+-------+-------------+----------+---------+--------+------------+---------+----+----+---------+--------------+-------------------+------------------+-----------+-------------+-------------------+----------------+------------------------+--------+---------------+------------------+----------+--------------------+
    |            player|   season|          team|games|games_starts|minutes|minutes_90s|goals|assists|goals_assists|goals_pens|pens_made|pens_att|cards_yellow|cards_red|  xg|npxg|xg_assist|npxg_xg_assist|progressive_carries|progressive_passes|goals_per90|assists_per90|goals_assists_per90|goals_pens_per90|goals_assists_pens_per90|xg_per90|xg_assist_per90|xg_xg_assist_per90|npxg_per90|npxg_xg_assist_per90|
    +------------------+---------+--------------+-----+------------+-------+-----------+-----+-------+-------------+----------+---------+--------+------------+---------+----+----+---------+--------------+-------------------+------------------+-----------+-------------+-------------------+----------------+------------------------+--------+---------------+------------------+----------+--------------------+
    |     David Abraham|2017-2018|Eint Frankfurt|   27|          27|   2302|       25.6|    0|      2|            2|         0|        0|       0|           3|        0| 0.4| 0.4|      0.7|           1.1|                 17|               103|        0.0|         0.08|               0.08|             0.0|                    0.08|    0.01|           0.03|              0.04|      0.01|                0.04|
    |      Amir Abrashi|2017-2018|      Freiburg|   12|          11|    850|        9.4|    0|      0|            0|         0|        0|       0|           2|        0| 0.2| 0.2|      0.4|           0.7|                  8|                38|        0.0|          0.0|                0.0|             0.0|                     0.0|    0.02|           0.05|              0.07|      0.02|                0.07|
    |        René Adler|2017-2018|      Mainz 05|   14|          14|   1260|       14.0|    0|      0|            0|         0|        0|       0|           0|        0| 0.0| 0.0|      0.3|           0.3|                  0|                 0|        0.0|          0.0|                0.0|             0.0|                     0.0|     0.0|           0.02|              0.02|       0.0|                0.02|
    |            Ailton|2017-2018|     Stuttgart|    5|           1|    108|        1.2|    0|      0|            0|         0|        0|       0|           0|        0| 0.0| 0.0|      0.1|           0.2|                  2|                 4|        0.0|          0.0|                0.0|             0.0|                     0.0|    0.03|           0.11|              0.14|      0.03|                0.14|
    |     Manuel Akanji|2017-2018|      Dortmund|   11|          10|    904|       10.0|    0|      0|            0|         0|        0|       0|           2|        0| 0.2| 0.2|      0.1|           0.3|                 15|                47|        0.0|          0.0|                0.0|             0.0|                     0.0|    0.02|           0.01|              0.03|      0.02|                0.03|
    |     Chadrac Akolo|2017-2018|     Stuttgart|   22|          13|   1102|       12.2|    5|      0|            5|         5|        0|       1|           2|        0| 4.7| 4.0|      1.0|           4.9|                 27|                35|       0.41|          0.0|               0.41|            0.41|                    0.41|    0.39|           0.08|              0.47|      0.32|                 0.4|
    |    Kevin Akpoguma|2017-2018|    Hoffenheim|   22|          17|   1690|       18.8|    0|      1|            1|         0|        0|       0|           1|        0| 0.2| 0.2|      1.4|           1.6|                 23|                85|        0.0|         0.05|               0.05|             0.0|                    0.05|    0.01|           0.07|              0.09|      0.01|                0.09|
    |       David Alaba|2017-2018| Bayern Munich|   23|          17|   1551|       17.2|    2|      2|            4|         2|        0|       0|           1|        0| 1.3| 1.3|      2.3|           3.5|                 53|               110|       0.12|         0.12|               0.23|            0.12|                    0.23|    0.07|           0.13|               0.2|      0.07|                 0.2|
    |      Lucas Alario|2017-2018|    Leverkusen|   23|          17|   1550|       17.2|    9|      4|           13|         8|        1|       2|           4|        1|10.5| 8.9|      1.8|          10.8|                 16|                28|       0.52|         0.23|               0.75|            0.46|                     0.7|    0.61|           0.11|              0.72|      0.52|                0.63|
    |    Miiko Albornoz|2017-2018|   Hannover 96|   10|           7|    703|        7.8|    0|      0|            0|         0|        0|       0|           1|        0| 0.2| 0.2|      1.4|           1.6|                 10|                25|        0.0|          0.0|                0.0|             0.0|                     0.0|    0.02|           0.18|              0.21|      0.02|                0.21|
    |  Thiago Alcántara|2017-2018| Bayern Munich|   19|          12|   1247|       13.9|    2|      2|            4|         2|        0|       0|           3|        0| 2.5| 2.5|      1.9|           4.4|                 30|               183|       0.14|         0.14|               0.29|            0.14|                    0.29|    0.18|           0.14|              0.32|      0.18|                0.32|
    | Stephan Ambrosius|2017-2018|  Hamburger SV|    1|           1|     45|        0.5|    0|      0|            0|         0|        0|       0|           0|        0| 0.0| 0.0|      0.0|           0.0|                  1|                 2|        0.0|          0.0|                0.0|             0.0|                     0.0|     0.0|            0.0|               0.0|       0.0|                 0.0|
    |      Nadiem Amiri|2017-2018|    Hoffenheim|   28|          19|   1744|       19.4|    2|      3|            5|         2|        0|       0|           4|        0| 2.9| 2.9|      3.4|           6.4|                 51|                89|        0.1|         0.15|               0.26|             0.1|                    0.26|    0.15|           0.18|              0.33|      0.15|                0.33|
    |    Waldemar Anton|2017-2018|   Hannover 96|   27|          26|   2278|       25.3|    1|      0|            1|         1|        0|       0|           1|        0| 1.8| 1.8|      0.0|           1.8|                 23|               101|       0.04|          0.0|               0.04|            0.04|                    0.04|    0.07|            0.0|              0.07|      0.07|                0.07|
    |       Dennis Aogo|2017-2018|     Stuttgart|   29|          22|   1954|       21.7|    0|      6|            6|         0|        0|       0|           5|        0| 1.3| 1.3|      2.3|           3.6|                 20|                85|        0.0|         0.28|               0.28|             0.0|                    0.28|    0.06|           0.11|              0.17|      0.06|                0.17|
    |  Charles Aránguiz|2017-2018|    Leverkusen|   27|          27|   2302|       25.6|    1|      3|            4|         1|        0|       0|           4|        0| 2.8| 2.8|      1.3|           4.1|                 26|               225|       0.04|         0.12|               0.16|            0.04|                    0.16|    0.11|           0.05|              0.16|      0.11|                0.16|
    | Maximilian Arnold|2017-2018|     Wolfsburg|   29|          28|   2454|       27.3|    2|      0|            2|         2|        0|       1|           9|        1| 2.3| 1.5|      2.9|           4.4|                 29|               148|       0.07|          0.0|               0.07|            0.07|                    0.07|    0.08|           0.11|              0.19|      0.05|                0.16|
    |    Jann-Fiete Arp|2017-2018|  Hamburger SV|   18|           8|    850|        9.4|    2|      0|            2|         2|        0|       0|           1|        0| 1.8| 1.8|      0.5|           2.3|                  9|                 5|       0.21|          0.0|               0.21|            0.21|                    0.21|    0.19|           0.05|              0.24|      0.19|                0.24|
    |      Takuma Asano|2017-2018|     Stuttgart|   15|           7|    721|        8.0|    1|      0|            1|         1|        0|       0|           1|        0| 1.7| 1.7|      1.1|           2.8|                 24|                17|       0.12|          0.0|               0.12|            0.12|                    0.12|    0.21|           0.13|              0.35|      0.21|                0.35|
    |Santiago Ascacíbar|2017-2018|     Stuttgart|   29|          27|   2381|       26.5|    0|      1|            1|         0|        0|       0|          11|        1| 0.4| 0.4|      0.7|           1.1|                 17|                92|        0.0|         0.04|               0.04|             0.0|                    0.04|    0.01|           0.03|              0.04|      0.01|                0.04|
    +------------------+---------+--------------+-----+------------+-------+-----------+-----+-------+-------------+----------+---------+--------+------------+---------+----+----+---------+--------------+-------------------+------------------+-----------+-------------+-------------------+----------------+------------------------+--------+---------------+------------------+----------+--------------------+
    only showing top 20 rows
    



```python
players_spark.count()
```




    18209



### Eliminación de Columnas no Necesarias

Nos quedaremos solo con las columnas que más aporten al entrenamiento.


```python
attributes.append('xg')
attributes
```




    ['games',
     'goals',
     'goals_assists',
     'goals_pens',
     'pens_att',
     'progressive_carries',
     'pens_made',
     'assists',
     'xg']




```python
players_spark = players_spark.select(attributes)
attributes = attributes[:-1]
players_spark.show()
```

    +-----+-----+-------------+----------+--------+-------------------+---------+-------+----+
    |games|goals|goals_assists|goals_pens|pens_att|progressive_carries|pens_made|assists|  xg|
    +-----+-----+-------------+----------+--------+-------------------+---------+-------+----+
    |   27|    0|            2|         0|       0|                 17|        0|      2| 0.4|
    |   12|    0|            0|         0|       0|                  8|        0|      0| 0.2|
    |   14|    0|            0|         0|       0|                  0|        0|      0| 0.0|
    |    5|    0|            0|         0|       0|                  2|        0|      0| 0.0|
    |   11|    0|            0|         0|       0|                 15|        0|      0| 0.2|
    |   22|    5|            5|         5|       1|                 27|        0|      0| 4.7|
    |   22|    0|            1|         0|       0|                 23|        0|      1| 0.2|
    |   23|    2|            4|         2|       0|                 53|        0|      2| 1.3|
    |   23|    9|           13|         8|       2|                 16|        1|      4|10.5|
    |   10|    0|            0|         0|       0|                 10|        0|      0| 0.2|
    |   19|    2|            4|         2|       0|                 30|        0|      2| 2.5|
    |    1|    0|            0|         0|       0|                  1|        0|      0| 0.0|
    |   28|    2|            5|         2|       0|                 51|        0|      3| 2.9|
    |   27|    1|            1|         1|       0|                 23|        0|      0| 1.8|
    |   29|    0|            6|         0|       0|                 20|        0|      6| 1.3|
    |   27|    1|            4|         1|       0|                 26|        0|      3| 2.8|
    |   29|    2|            2|         2|       1|                 29|        0|      0| 2.3|
    |   18|    2|            2|         2|       0|                  9|        0|      0| 1.8|
    |   15|    1|            1|         1|       0|                 24|        0|      0| 1.7|
    |   29|    0|            1|         0|       0|                 17|        0|      1| 0.4|
    +-----+-----+-------------+----------+--------+-------------------+---------+-------+----+
    only showing top 20 rows
    


### Convirtiendo el DataFrame de PySpark a Pandas


```python
players = players_spark.toPandas()
players
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>goals</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_att</th>
      <th>progressive_carries</th>
      <th>pens_made</th>
      <th>assists</th>
      <th>xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>27</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>17</td>
      <td>0</td>
      <td>2</td>
      <td>0.4</td>
    </tr>
    <tr>
      <th>1</th>
      <td>12</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>8</td>
      <td>0</td>
      <td>0</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>2</th>
      <td>14</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>11</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>0</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>18204</th>
      <td>5</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>7</td>
      <td>0</td>
      <td>0</td>
      <td>0.1</td>
    </tr>
    <tr>
      <th>18205</th>
      <td>4</td>
      <td>4</td>
      <td>4</td>
      <td>4</td>
      <td>0</td>
      <td>9</td>
      <td>0</td>
      <td>0</td>
      <td>0.5</td>
    </tr>
    <tr>
      <th>18206</th>
      <td>20</td>
      <td>5</td>
      <td>6</td>
      <td>4</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>1</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>18207</th>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>18208</th>
      <td>20</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>14</td>
      <td>0</td>
      <td>0</td>
      <td>0.2</td>
    </tr>
  </tbody>
</table>
<p>18209 rows × 9 columns</p>




## Preparación de los Datos para el Entrenamiento

### Mezcla de Datos


```python
players = players.sample(frac=1)
players
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>goals</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_att</th>
      <th>progressive_carries</th>
      <th>pens_made</th>
      <th>assists</th>
      <th>xg</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>17404</th>
      <td>26</td>
      <td>1</td>
      <td>6</td>
      <td>1</td>
      <td>0</td>
      <td>24</td>
      <td>0</td>
      <td>5</td>
      <td>0.8</td>
    </tr>
    <tr>
      <th>13658</th>
      <td>21</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>21</td>
      <td>0</td>
      <td>0</td>
      <td>0.9</td>
    </tr>
    <tr>
      <th>6825</th>
      <td>29</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>95</td>
      <td>0</td>
      <td>3</td>
      <td>1.1</td>
    </tr>
    <tr>
      <th>11165</th>
      <td>29</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>61</td>
      <td>1</td>
      <td>1</td>
      <td>2.8</td>
    </tr>
    <tr>
      <th>18040</th>
      <td>13</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>16</td>
      <td>0</td>
      <td>0</td>
      <td>0.2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1862</th>
      <td>26</td>
      <td>8</td>
      <td>19</td>
      <td>7</td>
      <td>1</td>
      <td>114</td>
      <td>1</td>
      <td>11</td>
      <td>6.6</td>
    </tr>
    <tr>
      <th>17260</th>
      <td>33</td>
      <td>13</td>
      <td>18</td>
      <td>10</td>
      <td>3</td>
      <td>12</td>
      <td>3</td>
      <td>5</td>
      <td>12.7</td>
    </tr>
    <tr>
      <th>3966</th>
      <td>30</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>21</td>
      <td>0</td>
      <td>2</td>
      <td>0.5</td>
    </tr>
    <tr>
      <th>3407</th>
      <td>17</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>31</td>
      <td>0</td>
      <td>0</td>
      <td>1.1</td>
    </tr>
    <tr>
      <th>8976</th>
      <td>29</td>
      <td>6</td>
      <td>14</td>
      <td>6</td>
      <td>0</td>
      <td>77</td>
      <td>0</td>
      <td>8</td>
      <td>5.3</td>
    </tr>
  </tbody>
</table>
<p>18209 rows × 9 columns</p>



### Separación de la matriz de características  X  de los datos de salida  y  (el target)


```python
y = players["xg"]
```


```python
y
```




    17404     0.8
    13658     0.9
    6825      1.1
    11165     2.8
    18040     0.2
             ... 
    1862      6.6
    17260    12.7
    3966      0.5
    3407      1.1
    8976      5.3
    Name: xg, Length: 18209, dtype: float64




```python
X = players[attributes]
```


```python
X
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>goals</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_att</th>
      <th>progressive_carries</th>
      <th>pens_made</th>
      <th>assists</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>17404</th>
      <td>26</td>
      <td>1</td>
      <td>6</td>
      <td>1</td>
      <td>0</td>
      <td>24</td>
      <td>0</td>
      <td>5</td>
    </tr>
    <tr>
      <th>13658</th>
      <td>21</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>21</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>6825</th>
      <td>29</td>
      <td>0</td>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>95</td>
      <td>0</td>
      <td>3</td>
    </tr>
    <tr>
      <th>11165</th>
      <td>29</td>
      <td>3</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>61</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>18040</th>
      <td>13</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>16</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>1862</th>
      <td>26</td>
      <td>8</td>
      <td>19</td>
      <td>7</td>
      <td>1</td>
      <td>114</td>
      <td>1</td>
      <td>11</td>
    </tr>
    <tr>
      <th>17260</th>
      <td>33</td>
      <td>13</td>
      <td>18</td>
      <td>10</td>
      <td>3</td>
      <td>12</td>
      <td>3</td>
      <td>5</td>
    </tr>
    <tr>
      <th>3966</th>
      <td>30</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>21</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>3407</th>
      <td>17</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>31</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>8976</th>
      <td>29</td>
      <td>6</td>
      <td>14</td>
      <td>6</td>
      <td>0</td>
      <td>77</td>
      <td>0</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
<p>18209 rows × 8 columns</p>




### Creación de los Datos de Entrenamiento y de Prueba


```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```


```python
X_train
```



<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>goals</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_att</th>
      <th>progressive_carries</th>
      <th>pens_made</th>
      <th>assists</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>15555</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9261</th>
      <td>6</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
      <td>16</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>4234</th>
      <td>29</td>
      <td>2</td>
      <td>3</td>
      <td>2</td>
      <td>0</td>
      <td>47</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>9979</th>
      <td>6</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>5</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7516</th>
      <td>20</td>
      <td>1</td>
      <td>3</td>
      <td>1</td>
      <td>0</td>
      <td>30</td>
      <td>0</td>
      <td>2</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>3164</th>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4222</th>
      <td>24</td>
      <td>2</td>
      <td>2</td>
      <td>2</td>
      <td>0</td>
      <td>16</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>17560</th>
      <td>11</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7329</th>
      <td>4</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>4</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>10088</th>
      <td>10</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>14567 rows × 8 columns</p>




```python
X_test
```


<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>games</th>
      <th>goals</th>
      <th>goals_assists</th>
      <th>goals_pens</th>
      <th>pens_att</th>
      <th>progressive_carries</th>
      <th>pens_made</th>
      <th>assists</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>8641</th>
      <td>5</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>16394</th>
      <td>27</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>9</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>6847</th>
      <td>14</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>14</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>7078</th>
      <td>33</td>
      <td>1</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>20</td>
      <td>0</td>
      <td>1</td>
    </tr>
    <tr>
      <th>10147</th>
      <td>16</td>
      <td>6</td>
      <td>6</td>
      <td>4</td>
      <td>2</td>
      <td>11</td>
      <td>2</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4289</th>
      <td>3</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>2</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>9723</th>
      <td>35</td>
      <td>1</td>
      <td>10</td>
      <td>1</td>
      <td>0</td>
      <td>56</td>
      <td>0</td>
      <td>9</td>
    </tr>
    <tr>
      <th>11648</th>
      <td>9</td>
      <td>1</td>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>6</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>11069</th>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>14038</th>
      <td>16</td>
      <td>0</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>15</td>
      <td>0</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
<p>3642 rows × 8 columns</p>




```python
y_train
```




    15555    0.0
    9261     0.7
    4234     3.3
    9979     0.5
    7516     2.1
            ... 
    3164     0.0
    4222     1.6
    17560    0.0
    7329     0.0
    10088    0.3
    Name: xg, Length: 14567, dtype: float64




```python
y_test
```




    8641     0.1
    16394    0.4
    6847     0.0
    7078     1.1
    10147    4.0
            ... 
    4289     0.1
    9723     0.7
    11648    0.3
    11069    0.0
    14038    0.7
    Name: xg, Length: 3642, dtype: float64



### Comprobación de Similitud entre Datos de Prueba y Datos de Entrenamiento


```python
X_train["goals"].hist(color='lightgreen', edgecolor="black")
plt.show()
```


    
![X_traingoals.hist](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_127_0.png)
    



```python
X_test["goals"].hist(color='lightgreen', edgecolor="black")
plt.show()
```


    
![X_testgoals.hist](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_128_0.png)
    



```python
X_train["assists"].hist(color='lightgreen', edgecolor="black")
plt.show()
```


    
![X_trainassists.hist](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_129_0.png)
    



```python
X_test["assists"].hist(color='lightgreen', edgecolor="black")
plt.show()
```


    
![X_testassists.hist](https://github.com/albertomorenogonzalez/ExpectedFoot/blob/main/media/graphics/output_130_0.png)
    


## Entrenamiento del Modelo y Comprobación del Rendimeinto

Usaremos Tres Modelos Distintos y nos quedaremso con el que se obtenga mejor rendimiento.

### Decision Tree


```python
from sklearn.tree import DecisionTreeRegressor

dt_model = DecisionTreeRegressor()

# Entrenamiento del modelo
dt_model.fit(X_train, y_train)

# Predicción
y_pred = dt_model.predict(X_test)

y_test_list = y_test.tolist()

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(20):
  r = y_test_list[i]
  e = y_pred[i]
  e_abs = abs(r - e)
  print(f"{r:10.2f}   {e:12.2f}  {e_abs:16.2f}")
```

    XG_Real    XG_Estimado   Error absoluto
          0.20           0.33              0.12
          0.00           0.01              0.01
          0.80           1.05              0.25
          0.50           0.30              0.20
          0.20           0.17              0.03
          6.80           9.10              2.30
          0.20           0.10              0.10
          0.10           0.17              0.07
          2.40           0.60              1.80
          2.00           1.40              0.60
          1.50           1.30              0.20
          1.10           0.38              0.73
          1.20           1.10              0.10
          0.30           0.12              0.18
          0.80           0.60              0.20
          0.00           0.05              0.05
          0.00           0.01              0.01
          0.00           0.01              0.01
          0.70           1.20              0.50
          2.60           1.70              0.90



```python
from sklearn.metrics import mean_squared_error, r2_score
```


```python
# Error
print("Error cuadrático medio: ", mean_squared_error(y_test, y_pred, squared=False))

# Coeficiente de determinación: 1 es la predicción perfecta.
print("Coeficiente de determinación: ", r2_score(y_test, y_pred))
```

    Error cuadrático medio:  1.2450269987871805
    Coeficiente de determinación:  0.8117366127168071


Ahora comporbaremos el resultado que obtiene al predecir los expected goals del top 10 de jugadores que obtuvimos previamente y veremos a ver cuantos de ellos aciertan (Lo haremos para cada modelo):


```python
pred = dt_model.predict(top_10_players[attributes])

xg_pred = top_10_players['xg'].to_list()

e_abs_count = []

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(10):
  r = pred[i]
  e = xg_pred[i]
  e_abs = abs(r - e)
  e_abs_count.append(e_abs)
  print(f"{r:10.2f}   {e:12.2f}  {e_abs:16.2f}")
```

]
0 s
pred = dt_model.predict(top_10_players[attributes])

xg_pred = top_10_players['xg'].to_list()

e_abs_count = []

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(10):
  r = pred[i]
  e = xg_pred[i]

    XG_Real    XG_Estimado   Error absoluto
         33.20          33.20              0.00
         31.30          31.30              0.00
         30.70          30.70              0.00
         30.70          30.70              0.00
         28.60          28.60              0.00
         28.40          28.40              0.00
         30.70          28.00              2.70
         27.90          27.90              0.00
         27.70          27.70              0.00
         27.20          27.20              0.00



```python
zero_num = [x for x in e_abs_count if x == 0]

# Calcula el porcentaje de ceros
zero_per = (len(zero_num) / len(e_abs_count)) * 100

print("Porcentaje de acierto:", zero_per, "%")
```

    Porcentaje de acierto: 90.0 %


### Random Forest


```python
from sklearn.ensemble import RandomForestRegressor

rf_model = RandomForestRegressor()

# Entrenamiento del modelo
rf_model.fit(X_train, y_train)

# Predicción
y_pred = rf_model.predict(X_test)

y_test_list = y_test.tolist()

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(20):
  r = y_test_list[i]
  e = y_pred[i]
  e_abs = abs(r - e)
  print(f"{r:10.2f}   {e:12.2f}  {e_abs:16.2f}")
```

    XG_Real    XG_Estimado   Error absoluto
          0.10           0.08              0.02
          0.40           1.68              1.28
          0.00           0.41              0.41
          1.10           1.29              0.19
          4.00           5.51              1.51
          0.20           0.48              0.28
          1.10           1.18              0.08
          0.00           0.01              0.01
          0.00           0.18              0.18
          2.40           4.08              1.68
          0.00           0.10              0.10
          0.70           0.79              0.09
          1.10           0.97              0.13
          0.50           0.37              0.13
          1.80           1.09              0.71
          1.20           1.06              0.14
          5.70           3.60              2.10
          0.00           0.03              0.03
          1.70           1.65              0.05
          0.10           0.31              0.21



```python
# Error
print("Error cuadrático medio: ", mean_squared_error(y_test, y_pred, squared=False))

# Coeficiente de determinación: 1 es la predicción perfecta.
print("Coeficiente de determinación: ", r2_score(y_test, y_pred))
```

    Error cuadrático medio:  1.0449520552112788
    Coeficiente de determinación:  0.8821879090921091



```python
pred = rf_model.predict(top_10_players[attributes])

xg_pred = top_10_players['xg'].to_list()

e_abs_count = []

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(10):
  r = pred[i]
  e = xg_pred[i]
  e_abs = abs(r - e)
  e_abs_count.append(e_abs)
  print(f"{r:10.2f}   {e:12.2f}  {e_abs:16.2f}")
```

    XG_Real    XG_Estimado   Error absoluto
         27.78          33.20              5.42
         27.54          31.30              3.76
         19.03          30.70             11.67
         28.80          30.70              1.90
         27.49          28.60              1.11
         27.40          28.40              1.00
         26.69          28.00              1.31
         26.30          27.90              1.60
         26.28          27.70              1.42
         26.65          27.20              0.55



```python
zero_num = [x for x in e_abs_count if x == 0]

# Calcula el porcentaje de ceros
zero_per = (len(zero_num) / len(e_abs_count)) * 100

print("Porcentaje de acierto:", zero_per, "%")
```

    Porcentaje de acierto: 0.0 %


### ANN (Artificial Neuronal Networks)


```python
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

# Escalar los datos para mejorar el rendimiento de la red neuronal
# scaler = StandardScaler()
# X_train_scaled = scaler.fit_transform(X_train)
# X_test_scaled = scaler.transform(X_test)

# Crear el modelo de Red Neuronal Artificial (MLPRegressor)
nn_model = MLPRegressor(hidden_layer_sizes=(100,), activation='relu', max_iter=1000, random_state=42)

# Entrenamiento del modelo
nn_model.fit(X_train, y_train)

# Predicción
y_pred_nn = nn_model.predict(X_test)

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(20):
    r = y_test_list[i]
    e = y_pred_nn[i]
    e_abs = abs(r - e)
    print(f"{r:10.2f}   {e:12.2f}  {e_abs:16.2f}")
```

    XG_Real    XG_Estimado   Error absoluto
          0.10           0.14              0.04
          0.40           1.24              0.84
          0.00           0.37              0.37
          1.10           1.30              0.20
          4.00           5.14              1.14
          0.20           0.83              0.63
          1.10           0.74              0.36
          0.00           0.01              0.01
          0.00          -0.03              0.03
          2.40           3.24              0.84
          0.00           0.08              0.08
          0.70           0.99              0.29
          1.10           1.20              0.10
          0.50           0.28              0.22
          1.80           0.94              0.86
          1.20           0.93              0.27
          5.70           3.22              2.48
          0.00           0.04              0.04
          1.70           1.74              0.04
          0.10           0.32              0.22



```python
rmse_nn = mean_squared_error(y_test, y_pred_nn, squared=False)
r2_nn = r2_score(y_test, y_pred_nn)

print("Error cuadrático medio (RMSE): ", rmse_nn)
print("Coeficiente de determinación: ", r2_score(y_test, y_pred))
```

    Error cuadrático medio (RMSE):  0.9759068784963901
    Coeficiente de determinación:  0.8821879090921091



```python
pred = nn_model.predict(top_10_players[attributes])

xg_pred = top_10_players['xg'].to_list()

e_abs_count = []

print("XG_Real    XG_Estimado   Error absoluto")
for i in range(10):
  r = pred[i]
  e = xg_pred[i]
  e_abs = abs(r - e)
  e_abs_count.append(e_abs)
  print(f"{r:10.2f}   {e:12.2f}  {e_abs:16.2f}")
```

    XG_Real    XG_Estimado   Error absoluto
         26.64          33.20              6.56
         31.05          31.30              0.25
         18.71          30.70             11.99
         27.00          30.70              3.70
         26.64          28.60              1.96
         28.32          28.40              0.08
         24.48          28.00              3.52
         23.56          27.90              4.34
         24.49          27.70              3.21
         29.63          27.20              2.43



```python
zero_num = [x for x in e_abs_count if x == 0]

# Calcula el porcentaje de ceros
zero_per = (len(zero_num) / len(e_abs_count)) * 100

print("Porcentaje de acierto:", zero_per, "%")
```

    Porcentaje de acierto: 0.0 %


## Elección del Modelo y Exportación

Hemos comprobado el rendimiento de todos los modelos y vemos que han obtenido resultados parecidos. Es cierto que el modelo de Decision Tree tiene un poco más de error y un poco menos de coeficiente de determinación, pero ha sido el capaz de acertar valores de forma exacta. Como ha demostrado ser el que mejor funciona dicidimos quedarnos con ese para exportarlo a la página web.


```python
import joblib
```


```python
joblib.dump(dt_model, "xg_prediction_model.pkl")
```




    ['xg_prediction_model.pkl']




```python
# Descarga del modelo
from google.colab import files

files.download('xg_prediction_model.pkl')
``` 


## Chatbot para la Web

Para la página web utilizaremos un ChatBot que interactuará con el usuario para pedir los datos por pantalla y mostrarle la predicción:

Puedes elegir para hablar con él en Español y en Inglés


```python
!pip install nltk googletrans==4.0.0-rc1
```

    Requirement already satisfied: nltk in /usr/local/lib/python3.10/dist-packages (3.8.1)
    Collecting googletrans==4.0.0-rc1
      Downloading googletrans-4.0.0rc1.tar.gz (20 kB)
      Preparing metadata (setup.py) ... [?25l[?25hdone
    Collecting httpx==0.13.3 (from googletrans==4.0.0-rc1)
      Downloading httpx-0.13.3-py3-none-any.whl (55 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m55.1/55.1 kB[0m [31m2.2 MB/s[0m eta [36m0:00:00[0m
    [?25hRequirement already satisfied: certifi in /usr/local/lib/python3.10/dist-packages (from httpx==0.13.3->googletrans==4.0.0-rc1) (2024.2.2)
    Collecting hstspreload (from httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading hstspreload-2024.2.1-py3-none-any.whl (1.1 MB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m1.1/1.1 MB[0m [31m7.0 MB/s[0m eta [36m0:00:00[0m
    [?25hRequirement already satisfied: sniffio in /usr/local/lib/python3.10/dist-packages (from httpx==0.13.3->googletrans==4.0.0-rc1) (1.3.0)
    Collecting chardet==3.* (from httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading chardet-3.0.4-py2.py3-none-any.whl (133 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m133.4/133.4 kB[0m [31m8.3 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting idna==2.* (from httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading idna-2.10-py2.py3-none-any.whl (58 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m58.8/58.8 kB[0m [31m8.1 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting rfc3986<2,>=1.3 (from httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading rfc3986-1.5.0-py2.py3-none-any.whl (31 kB)
    Collecting httpcore==0.9.* (from httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading httpcore-0.9.1-py3-none-any.whl (42 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m42.6/42.6 kB[0m [31m4.9 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting h11<0.10,>=0.8 (from httpcore==0.9.*->httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading h11-0.9.0-py2.py3-none-any.whl (53 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m53.6/53.6 kB[0m [31m6.0 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting h2==3.* (from httpcore==0.9.*->httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading h2-3.2.0-py2.py3-none-any.whl (65 kB)
    [2K     [90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[0m [32m65.0/65.0 kB[0m [31m8.7 MB/s[0m eta [36m0:00:00[0m
    [?25hCollecting hyperframe<6,>=5.2.0 (from h2==3.*->httpcore==0.9.*->httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading hyperframe-5.2.0-py2.py3-none-any.whl (12 kB)
    Collecting hpack<4,>=3.0 (from h2==3.*->httpcore==0.9.*->httpx==0.13.3->googletrans==4.0.0-rc1)
      Downloading hpack-3.0.0-py2.py3-none-any.whl (38 kB)
    Requirement already satisfied: click in /usr/local/lib/python3.10/dist-packages (from nltk) (8.1.7)
    Requirement already satisfied: joblib in /usr/local/lib/python3.10/dist-packages (from nltk) (1.3.2)
    Requirement already satisfied: regex>=2021.8.3 in /usr/local/lib/python3.10/dist-packages (from nltk) (2023.12.25)
    Requirement already satisfied: tqdm in /usr/local/lib/python3.10/dist-packages (from nltk) (4.66.2)
    Building wheels for collected packages: googletrans
      Building wheel for googletrans (setup.py) ... [?25l[?25hdone
      Created wheel for googletrans: filename=googletrans-4.0.0rc1-py3-none-any.whl size=17396 sha256=a25290ce220ab85552338fb3c886d2d99ce8c338fa2d29e2b076225ae1a082ca
      Stored in directory: /root/.cache/pip/wheels/c0/59/9f/7372f0cf70160fe61b528532e1a7c8498c4becd6bcffb022de
    Successfully built googletrans
    Installing collected packages: rfc3986, hyperframe, hpack, h11, chardet, idna, hstspreload, h2, httpcore, httpx, googletrans
      Attempting uninstall: chardet
        Found existing installation: chardet 5.2.0
        Uninstalling chardet-5.2.0:
          Successfully uninstalled chardet-5.2.0
      Attempting uninstall: idna
        Found existing installation: idna 3.6
        Uninstalling idna-3.6:
          Successfully uninstalled idna-3.6
    Successfully installed chardet-3.0.4 googletrans-4.0.0rc1 h11-0.9.0 h2-3.2.0 hpack-3.0.0 hstspreload-2024.2.1 httpcore-0.9.1 httpx-0.13.3 hyperframe-5.2.0 idna-2.10 rfc3986-1.5.0





```python
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
```

    Seleccione el idioma (español / inglés): español
    ExpectedFoot: ExpectedFoot
    ExpectedFoot: ¡Hola! Soy el asistente de ExpectedFoot, tu analizador de jugadores. Para comenzar, escribe 'comenzar'.
    Usuario: comenzar
    Usuario: comenzar
    Usuario: Introduce el nombre del jugador que desea analizar Roberto Fernández
    ExpectedFoot: Vamos a analizar al jugador Roberto Fernández
    Usuario: ¿Cuántos partidos ha jugado el jugador? 24
    ExpectedFoot: Roberto Fernández ha jugado 24 partidos.
    Usuario: ¿Cuántos goles ha marcado el jugador? 11
    ExpectedFoot: Roberto Fernández ha marcado 11 goles.
    Usuario: ¿Cuántas asistencias ha realizado el jugador? 4
    ExpectedFoot: Roberto Fernández ha realizado 4 asistencias de gol.
    ExpectedFoot: La suma de goles y asistencias juntas son 15
    Usuario: ¿Cuántos penaltis ha ejecutado el jugador? 1
    ExpectedFoot: Roberto Fernández ha tirado 1 penaltis
    Usuario: ¿Cuántos goles de penalti ha marcado el jugador de los 1 penaltis ejecutados? 1
    ExpectedFoot: Según los datos de goles de penalti, los goles marcados en jugadas son 10 goles
    Usuario: ¿Cuántos avances con la pelota hacia el área ha realizado con éxito? 40
    ExpectedFoot: Roberto Fernández ha regateado exitosamente 40 veces a jugadores cerca del aerea
    Roberto Fernández ha marcado 11 goles en 24 partidos, asistiendo 4 veces, ha ejecutado 1 penaltis, de los cuales ha marcado 1 y los goles marcados en jugada han sido 10.
     El resultado de los goles esperados del jugador es de 7.20 goles por temporada
