import requests
from time import sleep
from bs4 import BeautifulSoup
import pandas as pd

class Scraping: 

    def __init__(self) -> None:
        self.start()
        self.fildScraping()
   
    def start(self) -> None:
        url = 'https://lista.mercadolivre.com.br/'
        self.dados = []

        while True:
            search = str(input('O que deseja pesquisar no Mercado Liver? ')).strip().lower()
            if search:
                break

        url = url + search
        response = requests.get(url)
        self.site = BeautifulSoup(response.content, 'html.parser')
        sleep(2)
   
    def fildScraping(self) -> None:
        not_found = self.site.find('h3', attrs={'class': 'ui-search-rescue__title'}) 
        if not not_found: 
            produtos = self.site.findAll('div', attrs={'class': 'ui-search-result__wrapper shops__result-wrapper'}) 
            for produto in produtos:
                link = produto.find('a', attrs={'class': 'ui-search-item__group__element shops__items-group-details ui-search-link'})
                img = produto.find('img')
                descricao = produto.find('h2', attrs={'class': 'ui-search-item__title shops__item-title'})
                frete = produto.find('p', attrs={'class': 'ui-search-item__shipping ui-search-item__shipping--free shops__item-shipping-free'})
                preco_atual = produto.find('div', attrs={'class': 'ui-search-price__second-line shops__price-second-line'}).find('span', attrs={'class': 'price-tag-text-sr-only'})
                preco_antes = produto.find('span', attrs={'class': 'price-tag-text-sr-only'})
                
                if(frete):
                    self.dados.append([descricao.text, preco_antes.text, preco_atual.text, img.get('data-src'), link.get('href'), frete.text])
                else:
                    self.dados.append([descricao.text, preco_antes.text, preco_atual.text, img.get('data-src'), link.get('href'), 'Frete acombinar'])
        
            self.createFile()        
        else:
            print('Tente novamente!', not_found.text)
    
    def createFile(self) -> None:
        news = pd.DataFrame(self.dados, columns=['Descrição', 'Preço antes', 'Preço atual', 'Imagem', 'Link', 'Frete'])  
        news.to_csv('Scraping_Mercado_Livre.csv', index=False)


scraping = Scraping()






