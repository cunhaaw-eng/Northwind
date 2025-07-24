import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Northwind Analytics Dashboard", layout="wide", initial_sidebar_state="expanded")

# Estilo CSS para tema escuro mais intenso
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
        body { background-color: #262730; font-family: 'Roboto', sans-serif; color: #F5F5F5; }
        .stTabs [data-baseweb="tab-list"] { 
            gap: 16px; 
            background-color: #1F2A44; 
            padding: 10px; 
            border-bottom: 2px solid #4FC3F7; 
        }
        .stTabs [data-baseweb="tab"] { 
            border-radius: 10px; 
            padding: 12px 24px; 
            background-color: #1E3A8A; 
            color: #F5F5F5; 
            font-weight: 700; 
            font-size: 16px;
        }
        .stTabs [data-baseweb="tab"][aria-selected="true"] { 
            background-color: #4FC3F7; 
            color: #1F2A44; 
        }
        .metric-card { 
            background-color: #1E3A8A; 
            padding: 20px; 
            border-radius: 10px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.5); 
            margin-bottom: 20px; 
            text-align: center;
            border: 1px solid #4FC3F7;
        }
        .metric-title { font-size: 18px; color: #F5F5F5; margin-bottom: 10px; font-weight: 700; }
        .metric-value { font-size: 28px; font-weight: bold; color: #4FC3F7; }
        .plotly-chart { 
            border-radius: 15px; 
            overflow: hidden; 
            box-shadow: 0 2px 6px rgba(0,0,0,0.5); 
            border: 1px solid #4FC3F7; 
        }
        .stSelectbox, .stMultiSelect, .stDateInput { 
            background-color: #1F2A44; 
            border-radius: 8px; 
            padding: 10px; 
            margin-bottom: 10px; 
            border: 1px solid #4FC3F7;
        }
        .stSelectbox > div > div > div, .stMultiSelect > div > div > div { 
            font-weight: 700; color: #F5F5F5; 
        }
        h1, h2, h3, .subtitle { color: #4FC3F7; }
    </style>
""", unsafe_allow_html=True)

# Conexão com o banco PostgreSQL
@st.cache_resource
def get_data():
    engine = create_engine('postgresql://postgres:1581mcss!@localhost:5432/Northwind')
    metrics_query = "SELECT * FROM public_metrics.metrics"
    churn_query = "SELECT * FROM public_metrics.churns"
    df_metrics = pd.read_sql(metrics_query, engine)
    df_churn = pd.read_sql(churn_query, engine)
    return df_metrics, df_churn

# Carregar dados
df_metrics, df_churn = get_data()

# Filtros suspensos na sidebar
st.sidebar.header("Filtros de Análise")
with st.sidebar.expander("Intervalo de Datas", expanded=True):
    date_filter = st.date_input("Selecione o intervalo", [datetime(2000, 1, 1), datetime(2025, 12, 31)])

with st.sidebar.expander("Região", expanded=False):
    region_options = ['Todos'] + sorted(df_metrics['region'].unique().tolist())
    region_filter = st.multiselect("Selecione as regiões", options=region_options, default=['Todos'])
    if 'Todos' in region_filter:
        region_filter = df_metrics['region'].unique().tolist()

with st.sidebar.expander("Categoria", expanded=False):
    category_options = ['Todos'] + sorted(df_metrics['category_name'].unique().tolist())
    category_filter = st.multiselect("Selecione as categorias", options=category_options, default=['Todos'])
    if 'Todos' in category_filter:
        category_filter = df_metrics['category_name'].unique().tolist()

with st.sidebar.expander("Status do Cliente", expanded=False):
    status_options = ['Todos', 'Ativo', 'Inativo']
    status_filter = st.multiselect("Selecione o status", options=status_options, default=['Todos'])
    if 'Todos' in status_filter:
        status_filter = ['Ativo', 'Inativo']

with st.sidebar.expander("Produto", expanded=False):
    product_options = ['Todos'] + sorted(df_metrics['product_name'].unique().tolist())
    product_filter = st.multiselect("Selecione os produtos", options=product_options, default=['Todos'])
    if 'Todos' in product_filter:
        product_filter = df_metrics['product_name'].unique().tolist()

# Filtrar dados de metrics
filtered_df = df_metrics[
    (df_metrics['region'].isin(region_filter)) &
    (df_metrics['category_name'].isin(category_filter)) &
    (df_metrics['customer_status'].isin(status_filter)) &
    (df_metrics['product_name'].isin(product_filter))
]

# Título do dashboard
st.markdown("<h1 style='color: #4FC3F7; text-align: center;'>Northwind Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle' style='text-align: center;'>Análise estratégica para aumentar faturamento, reduzir churn e otimizar operações</p>", unsafe_allow_html=True)

# Abas do dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📊 KPIs", "💰 Faturamento", "📦 Estoque e Logística", "👥 Clientes"])

# --- Aba 1: KPIs (Visão Geral do Desempenho) ---
with tab1:
    st.markdown("<h2>KPI - Indicadores-Chave de Desempenho</h2>", unsafe_allow_html=True)
    st.markdown("Resumo do desempenho geral para monitorar metas de ticket médio, churn e eficiência operacional.", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Ticket Médio por Pedido</div>
                <div class="metric-value">R${filtered_df['avg_ticket_per_order'].mean():.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Ticket Médio por Cliente</div>
                <div class="metric-value">R${filtered_df['avg_ticket_per_customer'].mean():.2f}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Churn (6 Meses)</div>
                <div class="metric-value">{df_churn['churn_rate_6m'].iloc[0]:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">Churn (12 Meses)</div>
                <div class="metric-value">{df_churn['churn_rate_12m'].iloc[0]:.2f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<h3>Tendência do Ticket Médio por Região</h3>", unsafe_allow_html=True)
    fig_ticket_trend = px.bar(
        filtered_df.groupby('region')['avg_ticket_per_region'].mean().reset_index(),
        x='region', y='avg_ticket_per_region', title="Ticket Médio por Região",
        labels={'avg_ticket_per_region': 'Ticket Médio (R$)', 'region': 'País'},
        color='avg_ticket_per_region', color_continuous_scale=px.colors.sequential.Blues,
        text_auto='.2f'
    )
    fig_ticket_trend.update_layout(
        plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
        title_font_size=18, showlegend=True
    )
    st.plotly_chart(fig_ticket_trend, use_container_width=True)

# --- Aba 2: Faturamento (Onde Ganhamos Dinheiro) ---
with tab2:
    st.markdown("<h2>Faturamento - Análise de Receita</h2>", unsafe_allow_html=True)
    st.markdown("Explore a distribuição de receita por país, categoria e funcionário para identificar oportunidades de crescimento.", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        revenue_data = filtered_df.groupby('region')[['revenue_by_country', 'avg_ticket_per_region']].sum().reset_index()
        fig_revenue_country = go.Figure(data=[
            go.Bar(name='Receita por País', x=revenue_data['region'], y=revenue_data['revenue_by_country'], 
                   marker_color='#1E88E5', text=revenue_data['revenue_by_country'], textposition='auto'),
            go.Scatter(name='Ticket Médio', x=revenue_data['region'], y=revenue_data['avg_ticket_per_region'], 
                       mode='lines+markers+text', line=dict(color='#FFCA28'), text=revenue_data['avg_ticket_per_region'].round(2), 
                       textposition='top center')
        ])
        fig_revenue_country.update_layout(
            title="Receita e Ticket Médio por País", barmode='group',
            plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
            title_font_size=18, showlegend=True,
            yaxis_title="Receita (R$)", yaxis2=dict(title="Ticket Médio (R$)", overlaying='y', side='right')
        )
        st.plotly_chart(fig_revenue_country, use_container_width=True)
    
    with col2:
        fig_revenue_category = px.pie(
            filtered_df.groupby('category_name')['revenue_by_category'].sum().reset_index(),
            values='revenue_by_category', names='category_name', title="Receita por Categoria",
            color_discrete_sequence=['#1E88E5', '#BB86FC', '#FFCA28', '#2E7D32']
        )
        fig_revenue_category.update_traces(textinfo='percent+label')
        fig_revenue_category.update_layout(
            plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
            title_font_size=18, showlegend=True
        )
        st.plotly_chart(fig_revenue_category, use_container_width=True)
    
    fig_revenue_employee = px.bar(
        filtered_df.groupby('employee_name')['revenue_by_employee'].sum().reset_index().sort_values('revenue_by_employee', ascending=False).head(10),
        x='employee_name', y='revenue_by_employee', title="Top 10 Funcionários por Receita",
        color='revenue_by_employee', color_continuous_scale=px.colors.sequential.YlGn,
        labels={'revenue_by_employee': 'Receita (R$)', 'employee_name': 'Funcionário'},
        text_auto='.2s'
    )
    fig_revenue_employee.update_layout(
        plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
        title_font_size=18, showlegend=True
    )
    st.plotly_chart(fig_revenue_employee, use_container_width=True)

# --- Aba 3: Estoque e Logística (Eficiência Operacional) ---
with tab3:
    st.markdown("<h2>Estoque e Logística - Eficiência Operacional</h2>", unsafe_allow_html=True)
    st.markdown("Monitore estoques e tempos de entrega para reduzir custos e melhorar a experiência do cliente (ISO 9001).", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig_stock = go.Figure(data=[
            go.Bar(name='Baixo Estoque', x=['Total'], y=[filtered_df['low_stock_products'].sum()], marker_color='#FFCA28'),
            go.Bar(name='Alto Estoque', x=['Total'], y=[filtered_df['high_stock_products'].sum()], marker_color='#1E88E5'),
            go.Bar(name='Descontinuados com Vendas', x=['Total'], y=[filtered_df['discontinued_products_with_sales'].sum()], marker_color='#EF5350')
        ])
        fig_stock.update_layout(
            title="Status do Estoque", barmode='stack',
            plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
            title_font_size=18, showlegend=True,
            yaxis_title="Quantidade"
        )
        st.plotly_chart(fig_stock, use_container_width=True)
    
    with col2:
        fig_delivery_time = px.box(
            filtered_df, y='avg_delivery_time_days', title="Tempo Médio de Entrega (Dias)",
            labels={'avg_delivery_time_days': 'Dias'},
            color_discrete_sequence=['#1E88E5']
        )
        fig_delivery_time.update_layout(
            plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
            title_font_size=18, showlegend=True
        )
        st.plotly_chart(fig_delivery_time, use_container_width=True)
    
    fig_freight_cost = px.bar(
        filtered_df.groupby('shipper_name')['avg_freight_cost_by_shipper'].mean().reset_index(),
        x='shipper_name', y='avg_freight_cost_by_shipper', title="Custo Médio de Frete por Transportadora",
        color='avg_freight_cost_by_shipper', color_continuous_scale=px.colors.sequential.YlGn,
        labels={'avg_freight_cost_by_shipper': 'Custo Médio (R$)', 'shipper_name': 'Transportadora'},
        text_auto='.2f'
    )
    fig_freight_cost.update_layout(
        plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
        title_font_size=18, showlegend=True
    )
    st.plotly_chart(fig_freight_cost, use_container_width=True)
    
    st.markdown("<h3>Produtos com Necessidade de Reabastecimento por Região</h3>", unsafe_allow_html=True)
    restock_table = filtered_df.groupby('region')['frequent_restock_products_by_region'].sum().reset_index()
    restock_table['frequent_restock_products_by_region'] = restock_table['frequent_restock_products_by_region'].astype(int)
    st.dataframe(restock_table.style.set_properties(**{
        'background-color': '#1F2A44',
        'color': '#F5F5F5',
        'border-radius': '8px',
        'border': '1px solid #4FC3F7'
    }), use_container_width=True)

# --- Aba 4: Clientes (Fidelização e Churn) ---
with tab4:
    st.markdown("<h2>Clientes - Análise de Fidelização</h2>", unsafe_allow_html=True)
    st.markdown("Identifique clientes inativos e produtos mais vendidos para estratégias de retenção e promoções (ISO 9001).", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        fig_customer_status = px.pie(
            filtered_df.groupby('customer_status').size().reset_index(name='count'),
            values='count', names='customer_status', title="Distribuição de Status dos Clientes",
            color_discrete_sequence=['#2E7D32', '#FFCA28']
        )
        fig_customer_status.update_traces(textinfo='percent+label')
        fig_customer_status.update_layout(
            plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
            title_font_size=18, showlegend=True
        )
        st.plotly_chart(fig_customer_status, use_container_width=True)
    
    with col2:
        fig_top_products = px.bar(
            filtered_df.groupby('product_name')['quantity_sold'].sum().reset_index().sort_values('quantity_sold', ascending=False).head(10),
            x='product_name', y='quantity_sold', title="Top 10 Produtos Mais Vendidos",
            color='quantity_sold', color_continuous_scale=['#1E88E5', '#BB86FC'],
            labels={'quantity_sold': 'Quantidade Vendida', 'product_name': 'Produto'},
            text_auto=True
        )
        fig_top_products.update_layout(
            plot_bgcolor='#262730', paper_bgcolor='#262730', font_color='#F5F5F5',
            title_font_size=18, showlegend=True
        )
        st.plotly_chart(fig_top_products, use_container_width=True)
    
    st.markdown("<h3>Tabela de Clientes Inativos por Região</h3>", unsafe_allow_html=True)
    inactive_customers = (
        filtered_df[filtered_df['customer_status'] == 'Inativo']
        [['customer_id', 'customer_name', 'region']]
        .drop_duplicates()
    )
    st.dataframe(inactive_customers.style.set_properties(**{
        'background-color': '#1F2A44',
        'color': '#F5F5F5',
        'border-radius': '8px',
        'border': '1px solid #4FC3F7'
    }), use_container_width=True)