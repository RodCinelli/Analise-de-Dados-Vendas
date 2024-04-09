from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline

# Dados de vendas diárias de uma loja durante um mês (30 dias)
dados = {
    'Dia': range(1, 31),
    'Vendas': [
        150, 200, 250, 300, 100,
        400, 350, 300, 450, 200,
        250, 250, 300, 200, 100,
        400, 300, 350, 200, 250,
        200, 150, 400, 300, 250,
        350, 200, 150, 100, 300
    ]
}

df = pd.DataFrame(dados)

# Identificando a venda máxima e mínima
idx_max_vendas = df['Vendas'].idxmax()
valor_max_vendas = df['Vendas'][idx_max_vendas]
dia_max_vendas = df['Dia'][idx_max_vendas]

valor_min_vendas = df['Vendas'].min()
dias_min_vendas = df[df['Vendas'] == valor_min_vendas]['Dia'].tolist()

# Gráfico de vendas diárias
x_smooth = np.linspace(df['Dia'].min(), df['Dia'].max(), 300)
spl = make_interp_spline(df['Dia'], df['Vendas'], k=3)
y_smooth = spl(x_smooth)

fig_vendas_diarias = go.Figure()
fig_vendas_diarias.add_trace(go.Scatter(x=x_smooth, y=y_smooth, mode='lines+markers', name='Vendas', line=dict(color='royalblue')))

# Adicionar destaque para a venda máxima com anotação à direita
fig_vendas_diarias.add_trace(go.Scatter(
    x=[dia_max_vendas], y=[valor_max_vendas], mode='markers',
    marker=dict(color='green', size=12), name=f'Venda Máxima dia {dia_max_vendas}'
))
fig_vendas_diarias.add_annotation(
    x=dia_max_vendas, y=valor_max_vendas,
    text=f"Dia {dia_max_vendas}", showarrow=True, arrowhead=1, ax=40, ay=0
)

# Adicionar destaque para as vendas mínimas com anotações à direita
for dia in dias_min_vendas:
    venda_minima = df.loc[df['Dia'] == dia, 'Vendas'].values[0]
    fig_vendas_diarias.add_trace(go.Scatter(
        x=[dia], y=[venda_minima], mode='markers',
        marker=dict(color='red', size=12), name=f'Venda Mínima dia {dia}'
    ))
    
    # Mova as anotações para a direita
    fig_vendas_diarias.add_annotation(
        x=dia, y=venda_minima,
        text=f"Dia {dia}", showarrow=True, arrowhead=1, ax=40, ay=0
    )

# Configuração de layout para permitir destaque ao clicar nos itens da legenda
fig_vendas_diarias.update_layout(
    title='Vendas Diárias durante um Mês',
    xaxis_title='Dia',
    yaxis_title='Vendas',
    legend=dict(
        y=0.5,
        font=dict(size=12),
        itemsizing='constant'
    )
)

# Gráfico de vendas por categoria
categorias = ['Eletrônicos', 'Vestuário', 'Alimentos', 'Farmácia']
vendas_por_categoria = [500, 300, 400, 200]
fig_vendas_categoria = go.Figure(data=[go.Pie(labels=categorias, values=vendas_por_categoria, hole=.3)])
fig_vendas_categoria.update_layout(title='Vendas por Categoria')

def create_layout():
    return html.Div([
        html.H2('Análise de Vendas', className='titulo-analise-vendas'),
        dcc.Graph(figure=fig_vendas_diarias, id='grafico-vendas-diarias'),
        dcc.Graph(figure=fig_vendas_categoria, id='grafico-vendas-categoria')
    ], className='container')
