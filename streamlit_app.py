import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import plotly.express as px

API_URL = "http://127.0.0.1:5000"

st.set_page_config(layout="wide")

st.title("Dashboard de Clusterização Climática")
st.markdown("Use o controle deslizante abaixo para definir o número de clusters e visualize os resultados.")

# Selecionar número de clusters
k = st.slider("Número de clusters", 2, 12, 6)

# Botão para rodar a análise
if st.button("Rodar Análise"):
    st.info("Rodando a clusterização... Por favor, aguarde.")
    try:
        # Pega os dados dos clusters da API
        resp = requests.get(f"{API_URL}/clusters?k={k}")
        if resp.status_code == 200:
            df = pd.read_json(resp.text)
            st.success("Clusterização concluída!")

            # Exibe o mapa com clusters coloridos
            st.subheader("Mapa dos Clusters")
            fig_map = px.scatter_mapbox(
                df,
                lat="lat",
                lon="lon",
                color="cluster",
                color_continuous_scale=px.colors.cyclical.IceFire,
                size_max=15,
                zoom=2,
                mapbox_style="carto-positron"
            )
            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

            col1, col2 = st.columns(2)

            with col1:
                # Exibe a tabela com os resultados
                st.subheader("Dados dos Pontos (Amostra)")
                st.write(df.head())

            with col2:
                # Gráfico de barras da distribuição dos pontos por cluster
                st.subheader("Distribuição de Pontos por Cluster")
                counts = df["cluster"].value_counts().sort_index()
                fig_bar, ax = plt.subplots()
                counts.plot(kind="bar", ax=ax, color="skyblue")
                ax.set_xlabel("Cluster")
                ax.set_ylabel("Número de Pontos")
                st.pyplot(fig_bar)
            
            # Resumo dos valores médios por cluster
            st.subheader("Resumo dos Valores Médios por Cluster")
            resp_summary = requests.get(f"{API_URL}/resumo?k={k}")
            if resp_summary.status_code == 200:
                summary_data = resp_summary.json()
                summary_df = pd.DataFrame(summary_data)
                st.dataframe(summary_df)
            else:
                st.error(f"Erro ao buscar o resumo da API: {resp_summary.status_code}")
                st.write(resp_summary.text)

        else:
            st.error(f"Erro ao chamar a API: {resp.status_code}")
            st.write(resp.text)
    
    except requests.exceptions.ConnectionError as e:
        st.error(f"Não foi possível conectar à API. Certifique-se de que a API Flask está rodando em {API_URL}.")
        st.write(e)
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado: {e}")
