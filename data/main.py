from bs4 import BeautifulSoup
import requests
import pandas as pd

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
    links_info = []
    for link in matches:
        if link.a:
            links_info.append(link.a.get('href'))
    output_links = [links_info[i:i + 5] for i in range(0, len(links_info),5)]
    # equipos
    home_team = [link.get_text() for link in matches]
    output_text=[home_team[i:i + 13] for i in range(0, len(home_team), 13)]

    for item in output_text:
        for i in item:
            #print(i)
            if i == '':
                item.remove(i)
        # n += 1
        # print(n)
        # print('sublista: ',item)
        # print('longitud: ', len(item))
        if len(item)<=6:
            output_text.remove(item)

    return output_text, output_links


def team_detail(url, detail_matches, detail_link):
    #print(detail_matches)
    details = list(zip(detail_matches, detail_link))
    detail_team = []
    for item in details:
        detail_team.append(item[0]+item[1])
    select_team = input('Choose team: ')
    team = []
    
    for idx,item in enumerate(detail_team):
        for i in item:
            if select_team == i:
                team.append(detail_team[idx])

    return team[15]


def df_create(df_dict):
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
    for i in df_dict:
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

    df = pd.DataFrame(out_dict)
    #print(df.head())

    # guardar en archivo
    #df.to_csv('./data/raw/matches.csv')

    return df

def run():
    URL = 'https://fbref.com/es/partidos/'
    url = 'https://fbref.com'

    link_page = requests.get(URL)
    print(f'Respuesta HTTP: {link_page.status_code}')
    dict_list = leagues_list(url, link_page)
    league_pague = links_list(dict_list)
    output_text, output_link = detail_matches(url, league_pague)

    #df_create(output)
    print(team_detail(url, output_text, output_link))


if __name__=='__main__':
    run()