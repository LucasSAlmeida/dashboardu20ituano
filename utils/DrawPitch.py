import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Função que cria o campo
def create_pitch_plotly(length, width, unity, linecolor, df=None):
    if unity == "meters" and (length > 120 or width > 75):
        return "Dimensions too large for meters. Please use yards or reduce dimensions."
    elif unity == "yards" and (length > 130 or width > 100):
        return "Dimensions too large for yards. Maximum length is 130 yards and maximum width is 100 yards."

    # Criar a figura do campo
    fig = go.Figure()

    # Adiciona o campo de futebol
    fig.add_shape(type="rect", x0=0, y0=0, x1=length, y1=width, line=dict(color=linecolor))
    fig.add_shape(type="line", x0=length / 2, y0=0, x1=length / 2, y1=width, line=dict(color=linecolor))

    # Área de pênalti
    fig.add_shape(type="rect", x0=0, y0=(width / 2 - 16.5), x1=16.5, y1=(width / 2 + 16.5), line=dict(color=linecolor))
    fig.add_shape(type="rect", x0=length - 16.5, y0=(width / 2 - 16.5), x1=length, y1=(width / 2 + 16.5), line=dict(color=linecolor))

    # Área de 5 metros
    fig.add_shape(type="rect", x0=0, y0=(width / 2 - 5.5), x1=5.5, y1=(width / 2 + 5.5), line=dict(color=linecolor))
    fig.add_shape(type="rect", x0=length - 5.5, y0=(width / 2 - 5.5), x1=length, y1=(width / 2 + 5.5), line=dict(color=linecolor))

    # Círculo central e marca de pênalti
    fig.add_shape(type="circle", x0=(length / 2) - 9.15, y0=(width / 2) - 9.15, x1=(length / 2) + 9.15, y1=(width / 2) + 9.15, line=dict(color=linecolor))
    fig.add_shape(type="circle", x0=11 - 0.8, y0=(width / 2) - 0.8, x1=11 + 0.8, y1=(width / 2) + 0.8, fillcolor=linecolor)
    fig.add_shape(type="circle", x0=length - 11 - 0.8, y0=(width / 2) - 0.8, x1=length - 11 + 0.8, y1=(width / 2) + 0.8, fillcolor=linecolor)

    # Arcos de pênalti
    fig.add_shape(type="path", path=f'M 11,{width / 2} A 9.15,9.15 0 0,1 20.15,{width / 2}', line=dict(color=linecolor))
    fig.add_shape(type="path", path=f'M {length - 11},{width / 2} A 9.15,9.15 0 0,1 {length - 20.15},{width / 2}', line=dict(color=linecolor))

    # Configurações do layout
    fig.update_layout(
        title='Ações em campo',
        height=420,
        width=600,
        margin=dict(l=30, r=30, t=30, b=30),
        plot_bgcolor='white',
        dragmode=False,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )

    # Adiciona os pontos no campo, se fornecidos
    if df is not None:
        fig.add_trace(go.Scatter(
            x=df['x'], y=df['y'], mode='markers',
            marker=dict(size=10, color='red'),
            name='Posições dos Jogadores'
        ))

    return fig

# Layout da aplicação
st.title("Análise de Ações no Campo")

# Controle para selecionar o comprimento e a largura do campo
length = st.slider("Selecione o comprimento do campo", 90, 130, 105)
width = st.slider("Selecione a largura do campo", 60, 100, 68)

# Controle para selecionar a unidade
unity = st.selectbox("Selecione a unidade", ["yards", "meters"])

# Seleção da cor da linha
linecolor = st.color_picker("Selecione a cor das linhas", "#000000")

# Dados fictícios (você pode carregar os seus próprios)
data = {'x': [30, 50, 70], 'y': [20, 40, 60]}
df = pd.DataFrame(data)

# Gerar o gráfico do campo
fig = create_pitch_plotly(length, width, unity, linecolor, df)

# Exibir o gráfico no Streamlit
st.plotly_chart(fig)
