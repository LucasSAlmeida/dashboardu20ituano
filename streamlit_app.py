import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px
from utils.DrawPitch import create_pitch_plotly

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/main/eventos.csv')
df_grouped_by = df.groupby(['evento', 'posicao'])[['x']].count()
df_grouped_by.reset_index(inplace=True)

# Título da aplicação
st.title("Ituano Futebol Clube - Sub20")

# Dropdowns
selected_player = st.selectbox('Selecione um jogador', df.posicao.unique())
selected_game = st.selectbox('Selecione um jogo', df.jogo.unique())
selected_action = st.selectbox('Selecione uma ação', df.evento.unique())

# 1. Gráfico de Ações em Campo
st.subheader('Gráfico de Ações em Campo')
filtered_df = df[(df['posicao'] == selected_player) & (df['jogo'] == selected_game)]

if selected_action == 'Passe certo':
    filtered_passes = filtered_df[(filtered_df['evento'] == 'Passe certo')]
    
    # Criar figura do campo
    pitch_figure = create_pitch_plotly(120, 80, 'yards', 'black')
    
    # Adicionar setas de passes
    for _, row in filtered_passes.iterrows():
        pitch_figure.add_trace(
            go.Scatter(
                x=[row['x']],
                y=[row['y']],
                mode='lines+markers',
                line=dict(color='black', width=2),
                marker=dict(color='red', size=6),
                showlegend=False,
                hoverinfo='none',
            )
        )
        pitch_figure.add_annotation(
            x=row['x2'], 
            y=row['y2'], 
            ax=row['x'], 
            ay=row['y'],
            xref="x", 
            yref="y",
            axref="x", 
            ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor='black'
        )
else:
    filtered_action_df = filtered_df[(filtered_df['evento'] == selected_action)]
    pitch_figure = create_pitch_plotly(120, 80, 'yards', 'black', filtered_action_df)

st.plotly_chart(pitch_figure)

#2. Dados da Temporada
st.subheader('Gráfico de Barras de Ações na temporada')

# Filtrando os dados para o jogador selecionado
filtered_player_df = df[df['posicao'] == selected_player]

# Contagem das ações (eventos) do jogador
action_counts = filtered_player_df['evento'].value_counts().reset_index()
action_counts.columns = ['Evento', 'Quantidade']

# Criar gráfico de barras
bar_figure = px.bar(action_counts, x='Evento', y='Quantidade', 
                    title=f'Ações do Jogador {selected_player}', 
                    labels={'Quantidade': 'Número de Ações'}, 
                    color='Quantidade', 
                    color_continuous_scale='Viridis')

# Exibir o gráfico
st.plotly_chart(bar_figure)

# 3. Exibir Tabela das Ações do Jogador
st.subheader('Tabela de Ações do Jogador')

# Filtrando os dados para o jogador selecionado
filtered_player_df = df[df['posicao'] == selected_player]

# Contagem das ações (eventos) do jogador
action_counts = filtered_player_df['evento'].value_counts().reset_index()
action_counts.columns = ['Evento', 'Quantidade']

# Exibir a tabela
st.dataframe(action_counts)



