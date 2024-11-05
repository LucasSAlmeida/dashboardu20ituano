import streamlit as st
import pandas as pd
import plotly.graph_objects as go 
import plotly.express as px
from utils.DrawPitch import create_pitch_plotly

# Carregar os dados
df = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/main/eventos.csv')
df_grouped_by = df.groupby(['evento', 'posicao'])[['x']].count()
df_grouped_by.reset_index(inplace=True)

df_xT = pd.read_csv('https://raw.githubusercontent.com/LucasSAlmeida/dados/main/xT_ituano_despbrasil_s20_r1.csv')

# Título da aplicação
st.title("Ituano Futebol Clube - Sub20")

# Dropdowns
selected_player = st.selectbox('Selecione um jogador', df.posicao.unique())
selected_game = st.selectbox('Selecione um jogo', df.jogo.unique())
selected_action = st.selectbox('Selecione uma ação', df.evento.unique())

# 1. Gráfico de Ações em Campo
st.subheader('Gráfico de Ações em Campo')
filtered_df = df[(df['posicao'] == selected_player) & (df['jogo'] == selected_game)]

if selected_action == 'Passe':
    filtered_passes = filtered_df[(filtered_df['evento'] == 'Passe')]
    
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

# 2. Radar Plot por 90
st.subheader('Radar de Ações por 90')
filtered_grouped_df = df_grouped_by[df_grouped_by['posicao'] == selected_player]

# Preencher eventos ausentes com valor 0
all_events = df['evento'].unique()
for event in all_events:
    if event not in filtered_grouped_df['evento'].values:
        new_row = pd.DataFrame({'evento': [event], 'x': [0], 'posicao': [selected_player]})
        filtered_grouped_df = pd.concat([filtered_grouped_df, new_row], ignore_index=True)

filtered_grouped_df = filtered_grouped_df.sort_values('evento')
first_event = filtered_grouped_df.iloc[0]
filtered_grouped_df = pd.concat([filtered_grouped_df, pd.DataFrame([first_event])], ignore_index=True)

# Dividir os valores da coluna 'x' por 90
filtered_grouped_df['x'] = filtered_grouped_df['x'] / 90

# Gerar o gráfico radar
radar_figure = px.line_polar(filtered_grouped_df, r='x', theta='evento').update_layout(
    height=450, width=570, title=f'Radar de ações - {selected_player}', plot_bgcolor='black')
radar_figure.update_traces(line=dict(color='red'), fill='toself')

st.plotly_chart(radar_figure)


#3. Dados da Temporada
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



