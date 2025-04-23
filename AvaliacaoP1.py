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


# Criação de tabela HTML para exibição dos dados
tabela = '<table><thead>\
<tr><th colspan="9">Previsões de Ventos [Intervalo de 5 dias]</th></tr>\
<tr><th>Data</th><th>Rajada média do vento (10m)[km/h]</th><th>Rajada mínima do vento (10m)[km/h]</th>\
<th>Velocidade média do vento (10m)[km/h]</th><th>Velocidade mínima do vento (10m)[km/h]</th>\
<th>Probabilidade mínima de precipitação[mm]</th><th>Probabilidade média de precipitação[mm]</th>\
<th>Umidade Relativa média[%]</th><th>Temperatura Aparente Média[°C]</th></tr></thead>\
<tbody>'

for valores in dadosTabela:
    tabela += '<tr>\
    <td>'+str(valores['dataFormatada']) + '</td>\
    <td>'+str(valores['vento_rajada_media']) + '</td>\
    <td>'+str(valores['vento_rajada_min']) + '</td>\
    <td>'+str(valores['vento_velocidade_media']) + '</td>\
    <td>'+str(valores['vento_velocidade_min']) + '</td>\
    <td>'+str(valores['precipitacao_min']) + '</td>\
    <td>'+str(valores['precipitacao_media']) + '</td>\
    <td>'+str(valores['umidade_relativa_media']) + '</td>\
    <td>'+str(valores['temperatura_aparente_media']) + '</td>\
    </tr>'  
tabela += '</tbody></table>'
pagina = '<html><head> <meta charset="UTF-8">'
css = '<style> table{border-collapse: collapse; width:90%; }\
td, th { border: 1px solid #ddd; padding: 8px; font-size: 1.5em;}\
tr:nth-child(even){background-color: #f2f2f2;}\
tr:hover {background-color: #ddd;}\
td{text-align:center;}\
thead {padding-top: 12px; padding-bottom: 12px;background-color: 93adcf;\
color: black;}</style>'
pagina += css + '</head><body>'
pagina += '<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 20px;">'
pagina += '<div style="flex: 1; min-width: 300px;">'
pagina += '<h2>Gráfico: Umidade Relativa Média x Temperatura Aparente Média</h2>'
pagina += f'<img src="{grafico_nome}" alt="Gráfico Umidade x Temperatura" style="width:80%; max-width:800px;"><br><br>'
pagina += '</div>'
pagina += '<div style="flex: 1; min-width: 300px;">'
pagina += '<h2>Curva Delta T</h2>'
pagina += '<img src="https://th.bing.com/th/id/OIP.7htdfrG3_eU_WfPPl20ynAAAAA?rs=1&pid=ImgDetMain" alt="Curva Delta T" style="width:60%;">'
pagina += '</div>'
pagina += '</div>'

quadro_local = f'''
<div style="position: fixed; top: 20px; right: 20px; background-color: #eef; 
            padding: 15px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.2); 
            font-size: 1em; max-width: 250px; z-index: 999;">
    <strong>Local:</strong> {lugar}<br>
    <strong>Latitude:</strong> {latitude}<br>
    <strong>Longitude:</strong> {longitude}
</div>
'''

pagina += quadro_local 

pagina += tabela + '</body></html>'

arquivoHtml = open("AvaliacaoP1.html", "w", encoding="utf-8")
arquivoHtml.write(pagina)
arquivoHtml.close()


