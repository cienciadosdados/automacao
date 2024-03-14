import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np

# Adicionar a imagem no cabeçalho
image_url = "https://cienciadosdados.com/images/CINCIA_DOS_DADOS_4.png"
st.image(image_url, use_column_width=True)

# Adicionar o nome do aplicativo
st.subheader("Automação da Análise de Dados com IA")

# Componente interativo para upload
file_input = st.file_uploader("Upload a CSV file", type='csv')

# Função para carregar e exibir as 2 primeiras linhas dos dados do CSV
def load_and_preview_csv(file):
    if file is not None:
        df = pd.read_csv(file)
        st.write(df.head(2))  # Mostra apenas as duas primeiras linhas
        return df
    return None

df = load_and_preview_csv(file_input)

if df is not None:
    # Dropdown para escolher a variável (coluna) do DataFrame
    variavel = st.selectbox('Escolha a variável para análise:', df.columns)

    # Dropdown para escolher o tipo de gráfico
    tipo_grafico = st.selectbox('Escolha o tipo de gráfico:', ['Scatter Plot', 'Line Plot', 'Bar Chart', 'Histogram', 'Boxplot', 'Bubble Chart'])

    # Botão para gerar o gráfico
    if st.button('Gerar Gráfico'):
        if tipo_grafico == 'Scatter Plot':
            fig = px.scatter(df, x=variavel, y=df.columns[0] if df.columns[0] != variavel else df.columns[-1])
            st.plotly_chart(fig)
        elif tipo_grafico == 'Line Plot':
            fig = px.line(df, x=variavel, y=df.columns[0] if df.columns[0] != variavel else df.columns[-1])
            st.plotly_chart(fig)
        elif tipo_grafico == 'Bar Chart':
            fig = px.bar(df, x=variavel, y=df.columns[0] if df.columns[0] != variavel else df.columns[-1])
            st.plotly_chart(fig)
        elif tipo_grafico == 'Histogram':
            fig = px.histogram(df, x=variavel)
            st.plotly_chart(fig)
        elif tipo_grafico == 'Boxplot':
            fig = px.box(df, y=variavel)
            st.plotly_chart(fig)
        elif tipo_grafico == 'Bubble Chart':
            if len(df.columns) >= 3:
                fig = px.scatter(df, x=df.columns[0], y=variavel, size=df.columns[2], size_max=60)
                st.plotly_chart(fig)
            else:
                st.write("O DataFrame não tem colunas suficientes para criar o Bubble Chart.")

    # Botão para gerar clusters
    if st.button('Gerar Cluster com IA'):
        # Tratamento dos dados para KMeans
        X = df[['renda']].values
        kmeans = KMeans(n_clusters=5, random_state=0).fit(X)
        df['Cluster'] = kmeans.labels_

        # Criação do gráfico Boxplot para visualizar a distribuição da renda em cada cluster
        fig = px.box(df, x='Cluster', y='renda', color='Cluster', notched=True, 
                    title="Distribuição da Renda por Cluster")
        st.plotly_chart(fig)
