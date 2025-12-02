import streamlit as st
import pandas as pd
import plotly.express as px


car_data = pd.read_csv('vehicles.csv')
hist_button = st.button("Criar Histograma")

if hist_button: #  Se o botão for clicado
    #escrever uma mensagem
    st.write('Criando um histograma para o conjunto de dados de vendas de carros')
    #Criar o histograma
    fig = px.histogram(car_data, x="odometer")

    #exibir um grafico plotly interativo
    st.plotly_chart(fig, use_container_width=True)