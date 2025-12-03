import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# DATAFRAME (já existente no seu projeto)
# ---------------------------------------------------------
car_data = pd.read_csv("vehicles.csv")



# ---------------------------------------------------------
# TÍTULO / CABEÇALHO
# ---------------------------------------------------------
st.title("📊 Análise de Veículos – Visualizações Interativas")

st.write("""
Este painel permite analisar dados de veículos através de histogramas e gráficos de dispersão.
Use as caixas de seleção abaixo para escolher qual gráfico deseja visualizar.
""")

# ---------------------------------------------------------
# CHECKBOX 1 – HISTOGRAMA RELACIONANDO TYPE × BRAND
# ---------------------------------------------------------
st.subheader("📘 Histograma por Tipo e Marca")

build_hist_type_brand = st.checkbox("Criar histograma relacionando 'type' com 'brand'")

if build_hist_type_brand:
    st.write("Selecione um **type** para analisar suas marcas:")

    chosen_type = st.selectbox("Escolha o tipo de veículo:", car_data["type"].dropna().unique())

    filtered = car_data[car_data["type"] == chosen_type]

    st.write(f"### Distribuição de marcas dentro do tipo: **{chosen_type}**")

    fig, ax = plt.subplots()
    ax.hist(filtered["brand"], bins=len(filtered["brand"].unique()))
    ax.set_xlabel("Marca (brand)")
    ax.set_ylabel("Frequência")
    ax.set_title(f"Histograma de marcas para o tipo {chosen_type}")

    st.pyplot(fig)

# ---------------------------------------------------------
# CHECKBOX 2 – GRÁFICO DE DISPERSÃO model_year × price
# ---------------------------------------------------------
st.subheader("📗 Gráfico de Dispersão – Ano do Modelo vs Preço")

build_scatter = st.checkbox("Criar gráfico de dispersão entre 'model_year' e 'price'")

if build_scatter:
    st.write("### Dispersão entre Ano do Modelo e Preço")

    df_plot = car_data.dropna(subset=["model_year", "price"])

    fig, ax = plt.subplots()
    ax.scatter(df_plot["model_year"], df_plot["price"])
    ax.set_xlabel("Ano do Modelo")
    ax.set_ylabel("Preço (US$)")
    ax.set_title("Dispersão: Ano do Modelo vs Preço")

    st.pyplot(fig)

# ---------------------------------------------------------
# CHECKBOX 3 – MARCAS QUE POSSUEM OS CARROS MAIS CAROS
# ---------------------------------------------------------
st.subheader("📙 Histograma das Marcas com Carros Mais Caros")

build_hist_expensive = st.checkbox("Criar histograma das marcas com carros mais caros")

if build_hist_expensive:
    st.write("### Marcas com maiores preços médios")

    brand_prices = (
        car_data.groupby("brand")["price"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()
    ax.bar(brand_prices.index[:20], brand_prices.values[:20])  # Top 20 mais caras
    ax.set_xlabel("Marca")
    ax.set_ylabel("Preço médio (US$)")
    ax.set_title("Top 20 marcas com maiores preços médios")
    plt.xticks(rotation=70)