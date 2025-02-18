# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="GreenFlow Dashboard",
    page_icon="🌿",
    layout="wide"
)

# Carregar dados
df = pd.read_parquet('data/dados_sensores_5000.parquet')

# Título
st.title("🌿 GreenFlow - Dashboard de Sustentabilidade")

# Sidebar
st.sidebar.header("Filtros")
setor_select = st.sidebar.multiselect("Selecione os Setores:", df['setor'].unique())
data_range = st.sidebar.date_input(
    "Selecione o período:",
    [df['timestamp'].min(), df['timestamp'].max()]
)

# Aplicar filtros
mask = df['timestamp'].dt.date.between(data_range[0], data_range[1])
if setor_select:
    mask &= df['setor'].isin(setor_select)
df_filtered = df[mask]

# Métricas principais
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        "Consumo Médio de Energia",
        f"{df_filtered['consumo_energia'].mean():.2f} kWh"
    )
with col2:
    st.metric(
        "Consumo Médio de Água",
        f"{df_filtered['consumo_agua'].mean():.2f} m³"
    )
with col3:
    st.metric(
        "Emissão Média de CO2",
        f"{df_filtered['emissao_co2'].mean():.2f} kg"
    )

# Gráficos
col1, col2 = st.columns(2)

with col1:
    st.subheader("Consumo por Setor")
    fig_setor = px.box(
        df_filtered,
        x="setor",
        y="consumo_energia",
        title="Distribuição do Consumo de Energia por Setor"
    )
    st.plotly_chart(fig_setor, use_container_width=True)

with col2:
    st.subheader("Ranking de Empresas")
    empresa_rank = df_filtered.groupby('empresa')['consumo_energia'].mean().sort_values()
    fig_rank = px.bar(
        x=empresa_rank.index,
        y=empresa_rank.values,
        title="Consumo Médio por Empresa"
    )
    st.plotly_chart(fig_rank, use_container_width=True)

# Análise temporal
st.subheader("Consumo ao Longo do Tempo")
temporal = df_filtered.groupby(df_filtered['timestamp'].dt.date)['consumo_energia'].mean().reset_index()
fig_temporal = px.line(
    temporal,
    x='timestamp',
    y='consumo_energia',
    title="Tendência de Consumo de Energia"
)
st.plotly_chart(fig_temporal, use_container_width=True)

# Insights
st.subheader("📊 Principais Insights")
col1, col2 = st.columns(2)

with col1:
    st.write("**Top 3 Empresas Mais Eficientes:**")
    top_eficientes = empresa_rank.head(3)
    for empresa, consumo in top_eficientes.items():
        st.write(f"- {empresa}: {consumo:.2f} kWh")

with col2:
    st.write("**Top 3 Maiores Consumidores:**")
    top_consumidores = empresa_rank.tail(3)
    for empresa, consumo in top_consumidores.items():
        st.write(f"- {empresa}: {consumo:.2f} kWh")