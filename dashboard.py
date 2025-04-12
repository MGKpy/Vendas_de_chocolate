import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Chocolate Sales", layout='wide')

# Leitura e preparação dos dados
df = pd.read_csv("Chocolate_Sales_RealTime.csv", delimiter=',', decimal='.')
df = pd.DataFrame(df)
df['Amount'] = df['Amount'].replace(',', '.', regex=True).astype(float)
df["Date"] = df["Date"].replace('-', ' ', regex=True)
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date')
df['Date'] = df['Date'].dt.date
df['Month'] = df['Date'].apply(lambda x: str(x.year) + "-" + str(x.month).zfill(2))  # ex: 2022-01

# Sidebar com filtros
month = st.sidebar.select_slider("📅 Mês", sorted(df['Month'].unique()))
country = st.sidebar.selectbox("🌎 Estado", df['Country'].unique())

# Filtros aplicados
df_filtered = df[df['Month'] == month]
country_sales = df.groupby("Country")['Amount'].sum().reset_index()
country_filtered = country_sales[country_sales['Country'] == country]

# Layout principal
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# 🎯 Gráfico de faturamento por data (barra diária)
fig_date = px.bar(
    df_filtered,
    x='Date',
    y='Amount',
    title=f" Faturamento diário - {month}",
    text='Amount',
    color_discrete_sequence=['#636EFA']
)

fig_date.update_traces(
    texttemplate= 'R$ %{text:,.2f}',
    textposition='outside',
    textfont=dict(size=14, family='Arial Black', color='black')
)
fig_date.update_layout(
    title_font=dict(size=22, family='Arial Black'),
    xaxis_title="Data",
    yaxis_title="Faturamento (R$)",
    plot_bgcolor='white',
    bargap=0.3,
    uniformtext_minsize=12,
    uniformtext_mode='hide'
)
col1.plotly_chart(fig_date, use_container_width=True)

# 🎯 Gráfico de faturamento por estado (total)
fig_country = px.bar(
    country_sales.sort_values('Amount', ascending=False),
    x='Country',
    y='Amount',
    title="🏷️ Faturamento total por estado",
    text='Amount',
    color='Country',
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig_country.update_traces(
    texttemplate='R$ %{text:.2f}',
    textposition='outside',
    textfont=dict(size=14, family='Arial Black', color='black'),
    marker_line_width=1.5,
    marker_line_color='black'
)
fig_country.update_layout(
    title_font=dict(size=22, family='Arial Black'),
    xaxis_title="Estado",
    yaxis_title="Faturamento (R$)",
    plot_bgcolor='white',
    bargap=0.4,
    showlegend=False
)
col2.plotly_chart(fig_country, use_container_width=True)


person_sales = df.groupby("Sales Person")['Amount'].sum().reset_index()
fig_person_sales = px.pie(person_sales, values='Amount', names='Sales Person', title='Total de faturamento por vendedor')
col3.plotly_chart(fig_person_sales)

products_sales = df.groupby("Product")['Amount'].count().reset_index()
fig_product_count = px.histogram(products_sales,x='Product',y='Amount', title="Quantidade de produtos vendidos",text_auto=True)
fig_product_count.update_traces(
    
)
col4.plotly_chart(fig_product_count)

col5.dataframe(df)