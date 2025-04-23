# Obtenção as coordenadas (latitude e Longitude) de uma cidade

import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Obtenção da data atual e formatar data no formato brasileiro
dataAtual = datetime.now().strftime("%d/%m/%Y")


# Função para obter coordenadas geográficas (Setando url e parâmetros)
def obtencaoCoordenadas(nomeLugar):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': nomeLugar,   #"q"- query(nome do lugar)
        'format': 'json',  #format - formato de resposta
        'limit': 1     #limit - limite de resultados (compatíveis com o padrão da busca)
    }

    # Criação de cabeçalho para evitar possíveis bloqueios pelo servidor
    headers = {
        'User-Agent': 'Obtenção de geo-coordenadas'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        dados = response.json()
        if dados:
            latitude = dados[0]['lat']
            longitude = dados[0]['lon']
            return latitude, longitude
        else: 
            print(f"Nenhum resultado encontrado para '{nomeLugar}'.")
       


