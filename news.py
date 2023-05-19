import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://lista.mercadolivre.com.br/'
dados = []

while True:
    search = str(input('O que deseja pesquisar no Mercado Liver? ')).strip().lower()
    if search:
        break

url = url + search
response = requests.get(url)
site = BeautifulSoup(response.content, 'html.parser')
sleep(1)

produtos = site.findAll('div', attrs={'class': 'ui-search-result__wrapper shops__result-wrapper'})
for produto in produtos:
    link = produto.find('a', attrs={'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'})
    img = produto.get('img')
    descricao = produto.find('h2', attrs={'class': 'ui-search-item__title shops__item-title'})
    frete = produto.find('p', attrs={'class': 'ui-search-item__shipping ui-search-item__shipping--free shops__item-shipping-free'})
    preco_atual = produto.find('div', attrs={'class': 'ui-search-price__second-line shops__price-second-line'}).find('span', attrs={'class': 'price-tag-text-sr-only'})
    preco_antes = produto.find('span', attrs={'class': 'price-tag-text-sr-only'})
    
    if(frete):
        dados.append([descricao.text, preco_antes.text, preco_atual.text, link.get('href'), frete.text])
    else:
        dados.append([descricao.text, preco_antes.text, preco_atual.text, link.get('href'), 'Frete acombinar'])

news = pd.DataFrame(dados, columns=['Descrição', 'Preço antes', 'Preço atual', 'Link', 'Frete'])  
news.to_csv('Scraping_Mercado_Livre.csv', index=False)
    






