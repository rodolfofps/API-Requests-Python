# API-Requests-Python
Repository created by Git Codes to practice API requests with Python

# 🌤️ Previsão do Tempo e Análise Gráfica com Python

Este projeto em Python realiza a **consulta de dados meteorológicos** a partir do nome de uma cidade fornecido pelo usuário. Ele utiliza APIs públicas para obter:

- 📍 Coordenadas geográficas (latitude e longitude)
- 🌦️ Previsão do tempo para os próximos 5 dias
- 📊 Um gráfico relacionando umidade relativa média e temperatura aparente
- 🧾 Um arquivo HTML contendo a tabela com os dados

---

## 🚀 Funcionalidades

✅ Consulta automática de:

- Coordenadas geográficas via [OpenStreetMap Nominatim](https://nominatim.org/)
- Previsão do tempo via [Open-Meteo API](https://open-meteo.com/)
- Exibição tabular dos dados com HTML
- Geração e inserção de gráfico de dispersão com linha de tendência (regressão linear)
- Visualização de curva Delta T (estática)

---

## 🧠 Estrutura do Projeto

### 🔍 Etapas:

1. **📥 Entrada do usuário**  
   Solicita o nome de uma cidade, ex: `Bebedouro SP`

2. **🌍 Obtenção das coordenadas**  
   Utiliza a API Nominatim para buscar latitude e longitude da cidade.

3. **☁️ Coleta da previsão do tempo**  
   Chama a API Open-Meteo para buscar:
   - Rajadas de vento
   - Probabilidades de precipitação
   - Umidade relativa
   - Temperatura aparente

4. **📈 Geração de gráfico**
   - Usa `matplotlib` e `numpy` para criar um gráfico de dispersão da relação entre **umidade x temperatura**
   - Aplica uma **reta de tendência** (regressão linear)
   - Salva o gráfico como PNG

5. **🖥️ Geração de página HTML**
   - Monta uma tabela com todos os dados coletados
   - Insere o gráfico gerado
   - Adiciona uma imagem ilustrativa da **Curva Delta T**
   - Salva o arquivo como `AvaliacaoP1.html`

---

## 📊 Exemplo de Gráfico

<p align="center">
  <img src="Graph example.png" alt="Gráfico de Umidade vs Temperatura" width="500"/>
</p>

---

## 💻 Tecnologias Usadas

- `Python 3`
- `requests` – para chamadas HTTP
- `matplotlib` – para gráficos
- `numpy` – para regressão linear
- `datetime` – para manipulação de datas
- `HTML + CSS inline` – para geração da tabela

---

## 🧪 Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
