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
ligues_matches = web_body.find_all('div', attrs={
    'class':'table_wrapper tabbed'
    })
# links de cada liga
links_ligues = [url + link.a.get('href') for link in ligues_matches]
names_ligues = [link.a.text for link in ligues_matches]

# enpaquetar en diccionario
dict_links = {}
for n,l in zip(names_ligues,links_ligues):
    dict_links[n] = l

#print(dict_links)
# listar opciones
print('Options list:\n')
for idx,i in enumerate(dict_links.items()):
    print(f'[{idx + 1}] - {i[0]}')

#option = input('Escoge una liga: ')
#if option == 'A'