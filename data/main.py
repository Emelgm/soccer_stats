from bs4 import BeautifulSoup
import numpy as pd
import requests
import pandas as pd

URL = 'https://fbref.com/es/partidos/'
url = 'https://fbref.com'
LIGUES = ['Premier League', 'La Liga', 'Ligue 1', 'Bundesliga', 'Serie A']

web_page = requests.get(URL)
print(f'Respuesta HTTP: {web_page.status_code}')

# contenido html
content = web_page.text
# ordenar estructura html
web_body = BeautifulSoup(web_page.text, 'lxml')
# extraer partidos de ligas
leagues_matches = web_body.find_all('div', attrs={
    'class':'table_wrapper tabbed'
    })
# links de cada liga
links_leagues = [url + link.a.get('href') for link in leagues_matches]
names_leagues = [link.a.text for link in leagues_matches]

# enpaquetar en diccionario
dict_links = {}
for n,l in zip(names_leagues,links_leagues):
    dict_links[n] = l

#print(dict_links)
# listar opciones
name_list = []
number_list = []
print('\nOptions list:\n')
for idx,i in enumerate(dict_links.items()):
    print(f'[{idx + 1}] - {i[0]}')
    name_list.append(i[0])
    number_list.append(idx + 1)

# elegir opcion de liga
option = int(input('\nChoose a league: '))
try:
    if option == number_list[option - 1]:
        link_league = dict_links[name_list[option - 1]]
        print(f'Name League: {name_list[option - 1]}')
        league_page = requests.get(link_league)
        print(f'Respuesta HTTP: {league_page.status_code}')
except IndexError as e:
    print('\nindex out of range\ntry again')

# detalle de partidos
web_league = BeautifulSoup(league_page.text, 'lxml')
scores = web_league.find('div', attrs={
    'class': 'inactive'
}).find_all('li', attrs={
    'class': 'full'
})
# detalle de marcadores
link_score = url + scores[1].a.get('href')
link_matches = requests.get(link_score)
web_scores = BeautifulSoup(link_matches.text, 'lxml')
matches = web_scores.find('tbody').find_all('td')
home_team = [link.get_text() for link in matches]
output=[home_team[i:i + 13] for i in range(0, len(home_team), 13)]
out_dict = {
    'dia': '',
    'fecha': '',
    'hora': '',
    'equipo_local': '',
    'gx': '',
    'marcador': '',
    'gy': '',
    'equipo_visitante': '',
    'p': '',
    'estadio': '',
    'arbitro': '',
    'informe': '',
    'x': ''
}

# names_list = ['dia', 'fecha', 'hora', 'equipo_local', 'gx',
#     'marcador','gy', 'equipo_visitante', 'p', 'estadio', 'arbritro',
#     'informe'
# ]

dia_list = []
fecha_list = []
hora_list = []
el_list = []
gx_list = []
marcador_list = []
gy_list = []
ev_list = []
p_list = []
estadio_list = []
arbitro_list = []
inf_list = []
x_list = []
for i in output:
    dia_list.append(i[0])
    out_dict['dia'] = dia_list
    fecha_list.append(i[1])
    out_dict['fecha'] = fecha_list
    hora_list.append(i[2])
    out_dict['hora'] = hora_list
    el_list.append(i[3])
    out_dict['equipo_local'] = el_list
    gx_list.append(i[4])
    out_dict['gx'] = gx_list
    marcador_list.append(i[5])
    out_dict['marcador'] = marcador_list
    gy_list.append(i[6])
    out_dict['gy'] = gy_list
    ev_list.append(i[7])
    out_dict['equipo_visitante'] = ev_list
    p_list.append(i[8])
    out_dict['p'] = p_list
    estadio_list.append(i[9])
    out_dict['estadio'] = estadio_list
    arbitro_list.append(i[10])
    out_dict['arbitro'] = arbitro_list
    inf_list.append(i[11])
    out_dict['informe'] = inf_list
    x_list.append(i[12])
    out_dict['x'] = x_list
#print(out_dict)

df = pd.DataFrame(out_dict)
print(df.head())

# guardar en archivo
df.to_csv('./data/raw/matches.csv')

