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


def obtencaoPrevisaoTempo(latitude,longitude,nomeLugar):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'daily': 'wind_gusts_10m_mean,wind_speed_10m_mean,wind_gusts_10m_min,wind_speed_10m_min,precipitation_probability_min,precipitation_probability_mean,relative_humidity_2m_mean,apparent_temperature_mean',
        'timezone': 'America/Sao_Paulo',
        'forecast_days': 5
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        dadosPrevisao = response.json()
        # print(dadosPrevisao)
        print(f"\nData da consulta: {dataAtual}")
        print(f"Local: {nomeLugar}")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")
        print("\nPrevisão dos próximos 3 dias:")
    else:
        print("Erro ao obter a previsão do tempo:", response.status_code)

    #obtenção dos valores da consulta de cada parâmetro
    datas = dadosPrevisao['daily']['time']
    vento_rajada_media = dadosPrevisao['daily']['wind_gusts_10m_mean']
    vento_rajada_min = dadosPrevisao['daily']['wind_gusts_10m_min'] 
    vento_velocidade_media = dadosPrevisao['daily']['wind_speed_10m_mean']
    vento_velocidade_min = dadosPrevisao['daily']['wind_speed_10m_min']
    precipitacao_min = dadosPrevisao['daily']['precipitation_probability_min']
    precipitacao_media = dadosPrevisao['daily']['precipitation_probability_mean']
    umidade_relativa_media = dadosPrevisao['daily']['relative_humidity_2m_mean']
    temperatura_aparente_media = dadosPrevisao['daily']['apparent_temperature_mean']


    # Formatação da data obtida na requisição para o formato brasileiro
    dataFormatada = [datetime.strptime(datas, "%Y-%m-%d").strftime("%d/%m/%Y")
        for datas in dadosPrevisao['daily']['time']]
    
    dadosTabela = []

    #percorrer todos os dados de cada parâmetro e exibir os resultados	 
    for i in range(len(datas)):
     
        print(f"\nData: {dataFormatada[i]}")
        print(f"Rajada média do vento: {vento_rajada_media[i]} km/h")
        print(f"Rajada mínima do vento: {vento_rajada_min[i]} km/h")
        print(f"Velocidade média do vento: {vento_velocidade_media[i]} km/h")
        print(f"Velocidade mínima do vento: {vento_velocidade_min[i]} km/h")
        print(f"Precipitação mínima: {precipitacao_min[i]} mm")
        print(f"Precipitação média: {precipitacao_media[i]} mm")
        print(f"Umidade relativa média: {umidade_relativa_media[i]} %")
        print(f"Temperatura média: {temperatura_aparente_media[i]} °C")
        print("="*50)

        dadosTabela.append({
            'dataFormatada': dataFormatada[i],
            'vento_rajada_media': vento_rajada_media[i],
            'vento_rajada_min': vento_rajada_min[i],
            'vento_velocidade_media': vento_velocidade_media[i],
            'vento_velocidade_min': vento_velocidade_min[i],
            'precipitacao_min': precipitacao_min[i],
            'precipitacao_media': precipitacao_media[i],
            'umidade_relativa_media': umidade_relativa_media[i],
            'temperatura_aparente_media': temperatura_aparente_media[i]
        })

    return dadosTabela       


lugar = input("Informe o nome da cidade [Ex.: Bebedouro SP]: ") 
latitude, longitude = obtencaoCoordenadas(lugar)

if latitude and longitude:
    dadosTabela = obtencaoPrevisaoTempo(latitude, longitude, lugar)

#coleta de dados para plotagem do gráfico

umidades = [dia['umidade_relativa_media'] for dia in dadosTabela]
temperaturas = [dia['temperatura_aparente_media'] for dia in dadosTabela]
datas_labels = [dia['dataFormatada'] for dia in dadosTabela]

# Define os limites e os passos dos eixos
min_temp = 0
max_temp = 50
min_umi = 0
max_umi = 100

# Arredonda os limites para múltiplos de 5 e 10
xticks = np.arange(int(min_temp), int(max_temp)+5, 5)  
yticks = np.arange(int(min_umi), int(max_umi)+10, 10)  

# Criação do gráfico
plt.figure(figsize=(10,6))
# plt.plot(temperaturas, umidades, marker='o', linestyle='-', color='teal')
plt.scatter(temperaturas, umidades, color='teal', s=100, alpha=0.7, edgecolors='black')

for i, data in enumerate(datas_labels):
    plt.text(temperaturas[i], umidades[i], data, fontsize=9, ha='center')

coef = np.polyfit(temperaturas, umidades, 1)     
tendencia = np.poly1d(coef)                     
temperaturas_ordenadas = np.linspace(min(temperaturas), max(temperaturas), 100)
plt.plot(temperaturas_ordenadas, tendencia(temperaturas_ordenadas), color='red', linestyle='--', label='Tendência')

plt.title('Umidade Relativa Média x Temperatura Aparente Média')
plt.xlabel('Temperatura Aparente Média (°C)')
plt.ylabel('Umidade Relativa Média (%)')
plt.grid(True)

plt.xticks(xticks)
plt.yticks(yticks)

# Salvar o gráfico
grafico_nome = "grafico_umidade_vs_temperatura.png"
plt.tight_layout()
plt.savefig(grafico_nome)
plt.close()



