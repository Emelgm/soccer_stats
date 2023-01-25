from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

# ordenar estructura html
def leagues_list(url, url_web):
    web_body = BeautifulSoup(url_web.text, 'lxml')
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

    return dict_links


def links_list(links):
    # listar opciones
    name_list = []
    number_list = []
    print('\nOptions list:\n')
    for idx,i in enumerate(links.items()):
        print(f'[{idx + 1}] - {i[0]}')
        name_list.append(i[0])
        number_list.append(idx + 1)

    # elegir opcion de liga
    option = int(input('\nChoose a league: '))
    try:
        if option == number_list[option - 1]:
            link_league = links[name_list[option - 1]]
            print(f'Name League: {name_list[option - 1]}')
            league_page = requests.get(link_league)
            print(f'Respuesta HTTP: {league_page.status_code}')
    except IndexError as e:
        print('\nindex out of range\ntry again')
    
    return league_page


def detail_matches(url, url_web):
    # detalle de partidos
    web_league = BeautifulSoup(url_web.text, 'lxml')
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
    #rows = web_scores.find('tbody').find_all('tr')
    heads = web_scores.find('thead').find_all('th')
    head = [head.get_text() for head in heads]
    links_info = []
    for link in matches:
        if link.a:
            links_info.append(link.a.get('href'))
    output_links = [links_info[i:i + 5] for i in range(0, len(links_info),5)]
    # equipos
    home_team = [link.get_text() for link in matches]
    output_text=[home_team[i:i + len(head) - 2] for i in range(0, len(home_team), len(head) - 1)]

    # for item in output_text:
    #     for i in item:
    #         #print(i)
    #         if i == '':
    #             item.remove(i)
    #     # n += 1
    #     # print(n)
    #     # print('sublista: ',item)
    #     # print('longitud: ', len(item))
    #     if len(item)<=6:
    #         output_text.remove(item)

    return output_text, output_links, head[1:]


def team_detail(url, detail_matches, detail_link):
    #print(detail_matches)
    details = list(zip(detail_matches, detail_link))
    detail_team = []
    for item in details:
        detail_team.append(item[0]+item[1])
    select_team = input('Choose team: ')
    team = []
    date = datetime.today().strftime('%Y-%m-%d')
    
    for idx,item in enumerate(detail_team):
        for i in item:
            if select_team == i:
                #if item[1] <= date:
                team.append(detail_team[idx])

    return team


def df_file(data, headers):
    result = []
    for item in data:
        result.append(dict(zip(headers,item)))
    df=pd.DataFrame(result)
    #df.to_csv('./data/raw/matches.csv')

    return df


def run():
    URL = 'https://fbref.com/es/partidos/'
    url = 'https://fbref.com'

    link_page = requests.get(URL)
    print(f'Respuesta HTTP: {link_page.status_code}')
    # listado de ligas disponibles
    dict_list = leagues_list(url, link_page)
    league_pague = links_list(dict_list)
    # tablas de marcadores y links
    output_text, output_link, head = detail_matches(url, league_pague)
    # filtrar historial por equipo
    print(team_detail(url, output_text, output_link))
    # generar dataframe
    #print(df_file(output_text, head))


if __name__=='__main__':
    run()