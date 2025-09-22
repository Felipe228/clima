# clima
Para baixar os dados e entendê-los: https://sites.google.com/site/alexandrecandidoxavierufes/brazilian-daily-weather-gridded-data
Códigos utilizados na extração de dados climáticos.
Este projeto consiste em uma arquitetura de duas partes para análise de dados climáticos e visualização interativa. A API realiza a clusterização dos dados, enquanto o dashboard exibe os resultados.
Tecnologias

    API: Flask, xarray, scikit-learn

    Dashboard: Streamlit, requests, plotly-express

Como Rodar

Para executar a aplicação, rode a API e Dashboard em terminais separados.
Pré-requisitos

    Python 3.8+

    Arquivos de dados .nc na raiz do projeto.

Passo 1: Instalação

Instale as dependências:

pip install flask xarray pandas numpy scikit-learn netcdf4
pip install streamlit matplotlib requests plotly-express

Passo 2: Rodar o Backend

Abra um primeiro terminal e execute os comandos:

python api.py

O servidor será iniciado. Mantenha este terminal ativo.
Passo 3: Rodar o Frontend

Abra um segundo terminal e inicie o dashboard:

python -m streamlit run streamlit_app.py

A aplicação será carregada no navegador.
