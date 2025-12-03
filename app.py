import streamlit as st 
import pandas as pd
import plotly.express as px

st.title("📊 Analise Exploratória de dados - vendas de Veiculos")

# ==========================================================
# 1) PREPARAÇÃO DOS DADOS
# ==========================================================
car_data = pd.read_csv("vehicles.csv")
# Criar coluna 'brand' pegando apenas a primeira palavra do modelo
car_data["brand"] = car_data["model"].str.split().str[0]

# Remover linhas sem "type"
car_data = car_data.dropna(subset=["type"])

# Lista de tipos únicos
all_types = sorted(car_data["type"].unique())

# Paleta de cores
color_map = {
    "SUV": "green",
    "pickup": "red",
    "sedan": "blue",
    "truck": "orange",
    "coupe": "purple",
    "van": "brown",
    "convertible": "pink",
    "hatchback": "yellow",
    "wagon": "cyan",
    "mini-van": "olive",
    "other": "gray",
    "offroad": "black"
}

# ==========================================================
# 2) MULTISELECT PARA O USUÁRIO ESCOLHER QUIS TYPES VER
# ==========================================================

st.subheader("Selecione os tipos de veículos para exibir")

selected_types = st.multiselect(
    "Selecione os tipos:",
    options=all_types,
    default=["SUV", "pickup"]
)

# Filtrar seleção
filtered = car_data[car_data["type"].isin(selected_types)]

# ==========================================================
# 3) GRÁFICO BARRA EMPILHADA brand × type
# ==========================================================

if len(filtered) == 0:
    st.warning("Selecione ao menos um tipo de veículo.")
else:
    st.subheader("🚗 Distribuição dos Tipos de Veículos por Marca")

    fig = px.histogram(
        filtered,
        x="brand",
        color="type",
        barmode="stack",
        color_discrete_map=color_map
    )

    fig.update_layout(
        xaxis_title="Marca",
        yaxis_title="Quantidade",
        bargap=0.15,
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)

# ==========================================================
# 4) GRÁFICO DE DISPERSÃO model_year × price
# ==========================================================

st.subheader("📈 Relação Entre Ano do Modelo e Preço")

fig_scatter = px.scatter(
    car_data,
    x="model_year",
    y="price",
    color="brand",
    opacity=0.7,
    height=450
)

st.plotly_chart(fig_scatter, use_container_width=True)


# ==========================================================
# 5) MELHORIA — MARCAS COM MAIORES PREÇOS MÉDIOS
# ==========================================================

st.subheader("💰 Top Marcas com Maiores Preços Médios")

# Garantir tipos
car_data = car_data.dropna(subset=["price", "brand"])
car_data["price"] = car_data["price"].astype(float)

# Calcular média
brand_mean_price = (
    car_data.groupby("brand")["price"]
    .mean()
    .sort_values(ascending=False)
    .reset_index()
)

# Top 10
top_n = 10
top_brands = brand_mean_price.head(top_n)

# Gráfico
fig_bar = px.bar(
    top_brands,
    x="Preço",
    y="Marca",
    orientation="h",
    text=top_brands["price"].round(0),
    height=500
)

fig_bar.update_layout(
    xaxis_title="Preço Médio (R$)",
    yaxis_title="Marca",
    title=f"Top {top_n} Marcas com Maiores Preços Médios"
)

st.plotly_chart(fig_bar, use_container_width=True)

# Mostrar tabela
st.dataframe(top_brands)