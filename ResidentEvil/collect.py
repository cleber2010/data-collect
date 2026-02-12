# %%
#deixar a estrutura para coletar dados de outros personagens
#limpeza dos dados em outro arquivo

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd

headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'referer': 'https://www.residentevildatabase.com/personagens/',
        'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Mobile Safari/537.36',
        # 'cookie': '_gid=GA1.2.382082318.1770760287; _ga=GA1.1.830293796.1770760257; __gads=ID=adc5b329720078d8:T=1770834681:RT=1770834681:S=ALNI_MYQI9LU4398dYAbI0BnI7Nq04IkEA; __eoi=ID=4eb51cbf4ed8e7cf:T=1770834681:RT=1770834681:S=AA-AfjYfM7DldfW42ifQo1td0CCN; _ga_DJLCSW50SC=GS2.1.s1770834640$o2$g1$t1770834683$j49$l0$h0; _ga_D6NF5QC4QT=GS2.1.s1770834640$o2$g1$t1770834683$j49$l0$h0; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B32%2C%22%5B%5C%226971d616-708a-447a-8b1b-60f7efe088e3%5C%22%2C%5B1770760256%2C722000000%5D%5D%22%5D%5D%5D; FCNEC=%5B%5B%22AKsRol9jHL9XgxlC_dBHJk8vUHaQImPXTDXn42GQVwfDLSjlWaw_cnKb4HRMhljBCK7vDXwgoB1qOuGrMzLiy6yi5ZJALoeamgPlBUSIzEdbKw_b1Uj_YugDLsF1p5G-Ojcw3h6UWknDd_C2SrFb_TAD6KrKJCNTpQ%3D%3D%22%5D%5D',
    }

# %%
def get_content(url):   
    response = requests.get(url, headers=headers)
    return response 

# %%
def get_basic_infos(soup):

    div_page = soup.find("div", {"class": "td-page-content"})
    paragrafo = div_page.find_all("p")[1]
    ems = paragrafo.find_all("em")
    # Percorre os elementos "chave:valor", separa pelo ":" e monta o dicionário data.
    data = {}
    for i in ems:
        chave, valor, *_= i.text.split(":")
        chave = chave.strip(" ")
        data[chave] = valor.strip(" ")
    return data
# %%
def get_appearances(soup):
    lis = (soup.find("div", {"class": "td-page-content"})
                .find("h4")
                .find_next()
                .find_all("li"))

    aparicoes = []
    for li in lis:
        aparicoes.append(li.text)
    return aparicoes

# %%
def get_personage_infos(url):

    response = get_content(url)
    if response.status_code != 200:
        print("Requisição mal-sucedida!", response.status_code)
        return {}
    else:
        soup = BeautifulSoup(response.text)
        data = get_basic_infos(soup)
        data["Aparições"] = get_appearances(soup)
        return data
# %%    
def get_links_personagens():
    url = "https://www.residentevildatabase.com/personagens"
    response = requests.get(url, headers=headers)
    soup_personagens = BeautifulSoup(response.text, 'html.parser')
    ancoras = soup_personagens.find("div", {"class": "td-page-content"}).find_all("a")
    links = []
    for i in ancoras:
        links.append(i['href'])
    return links

# %%
links = get_links_personagens()
data = []
for i in tqdm(links):
    d = get_personage_infos(i)
    d["Link"] = i
    nome = i.strip("/").split("/")[-1].replace("-", " ").title()
    d["Nome"] = nome
    data.append(d)

# %%
df = pd.DataFrame(data)
df
# %%
df.to_csv("personagens.csv", index=False, sep=";")
# %%
df.to_parquet("personagens.parquet", index=False)
# %%
df_new = pd.read_parquet("personagens.parquet")
# %%
df_new
# %%
