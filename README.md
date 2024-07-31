# ProjectCaiena
## Descrição
ProjectCaiena é uma aplicação desenvolvida em FastAPI que integra-se com os serviços OpenWeatherMap e Twitter. A aplicação permite enviar um tweet com a temperatura atual e a previsão dos próximos cinco dias (média diária) de uma cidade específica.

## Funcionalidades
- Obter Temperatura e Previsão do Tempo: Integração com a API do OpenWeatherMap para obter dados meteorológicos.
- Publicação no Twitter: Integração com a API do Twitter para publicar tweets com as informações do tempo.
## Estrutura do Projeto

```plaintext
ProjectCaiena/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── openweathermap.py
│   ├── twitter_sdk.py
│
├── tests/
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_openweathermap.py
│   ├── test_twitter_sdk.py
│
├── .env
├── config.py
├── requirements.txt
├── run.py
```
## Diretório app/
 - main.py: Implementa a API utilizando FastAPI. Define os endpoints para receber dados de cidades e processar informações meteorológicas.
 - openweathermap.py: SDK para comunicação com a API do OpenWeatherMap
 - twitter.py: SDK para interação com a API do Twitter.
## Diretório tests/
Contém testes automatizados para verificar o funcionamento correto dos componentes da aplicação.

## Arquivos Adicionais
- .env: Arquivo para variáveis de ambiente (não deve ser versionado).
- config.py: Configurações do projeto.
- requirements.txt: Lista de dependências do projeto.
- run.py: Script para iniciar a aplicação com Uvicorn.
# Instalação
 1. Clone o repositório:

```plaintext
git clone https://github.com/seuusuario/ProjectCaiena.git
cd ProjectCaiena
```
2. Crie e ative um ambiente virtual:
- No Windows:
```plaintext
python -m venv venv
venv\Scripts\activate
```
- No macOS e Linux:
```plaintext
python3 -m venv venv
source venv/bin/activate
```
3. Instale as dependências:

```plaintext
pip install -r requirements.txt
```
4. Configuração das Variáveis de Ambiente
- Crie um arquivo .env na raiz do projeto e adicione as seguintes variáveis:

```plaintext
OPENWEATHER_API_KEY=your_openweather_api_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET_KEY=your_twitter_api_secret_key
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token
```
## Uso
Para iniciar a aplicação, execute:

```plaintext
python run.py
```
A API estará disponível em http://127.0.0.1:8000.

## Endpoints Disponíveis
 - POST /weather: Recebe o nome de uma cidade e retorna a temperatura atual e a previsão para os próximos cinco dias.
- Exemplo de Requisição
```plaintext
POST /weather
{
  "city": "São Paulo"
}
```
- Exemplo de Resposta
```plaintext
{
  "formatted_weather": "25°C e céu limpo em São Paulo em 01/01. Média para os próximos dias: 22°C em 02/01, 23°C em 03/01, 24°C em 04/01, 25°C em 05/01, 26°C em 06/01."
}
```

## Testes
Para rodar os testes, utilize Pytest:

```plaintext
pytest
```

## Licença
Este projeto está licenciado sob os termos da licença MIT.

