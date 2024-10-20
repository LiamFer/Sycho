import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
import streamviz
from wordcloud import WordCloud
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")


def page2():
    # Puxando o Arquivo com as Infos
    FILEPATH = r"C:\\Users\\Windows\\Desktop\\cc.xlsx"
    df = pd.read_excel(FILEPATH)

    # Função pro Gráfico do Plotly
    def create_plotly_graph(data):
        x_values = df["Data e Horário"]
        y_values = df["Quantidade"]
        print(y_values)
        colors = ["red" if y >= 4 else "green" for y in y_values]

        fig = go.Figure(
            data=go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                marker=dict(size=12, color=colors),
                line=dict(color="gray"),
            )
        )

        fig.update_layout(
            title="QTD de Comida Consumida",
            xaxis_title="Data",
            yaxis_title="Quantidade (KG)",
        )

        return fig

    col1, col2 = st.columns(2)

    with col1:
        # Create some sample text
        text = 'Fun, fun, awesome, awesome, tubular, astounding, superb, great, amazing, amazing, amazing, amazing'

        # Create and generate a word cloud image:
        wordcloud = WordCloud().generate(text)
        
        # Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        st.pyplot()
        
        # streamviz.gauge(
        #     0.92,
        #     gTitle="KPI Indicator",
        #     gSize="MED",
        #     sFix="%",
        #     gcHigh="#21b581",
        #     gcLow="#de8a31",
        #     gcMid="#f5d02f",
        #     gTheme="#ffffff",
        # )
        
    # Puxando os Alimentos mais consumidos pela Pessoa
    food = {
        "Alimentos": [
            k.strip().title() for i in df["Alimentos Consumidos"].str.split(",").to_numpy() for k in i
        ],
    }
    food = pd.DataFrame(food)
    mostConsumedItems = (
        food.groupby("Alimentos")["Alimentos"]
        .count()
        .reset_index(name="count")
        .sort_values(["count"], ascending=False)
        .head(3)
        .to_numpy()
    )

    with col2:
        st.header("Ranking Principais Alimentos:")
        st.divider()
        col1, col2, col3 = st.columns(3)
        col1.metric(
            "O Mais Consumido",
            mostConsumedItems[0][0],
            f"{mostConsumedItems[0][1]} Vezes",
            delta_color="off",
        )
        col2.metric(
            "Segundo mais Consumido",
            mostConsumedItems[1][0],
            f"{mostConsumedItems[1][1]} Vezes",
            delta_color="off",
        )
        col3.metric(
            "Terceiro mais Consumido",
            mostConsumedItems[2][0],
            f"{mostConsumedItems[2][1]} Vezes",
            delta_color="off",
        )
        fig = create_plotly_graph(df)
        st.plotly_chart(fig)

pg = st.navigation(
    {
        "Escolha uma Opção": [
            st.Page(page2, title="Overview", icon="📌"),
            st.Page("page1.py", title="Diário", icon="📝"),
        ]
    }
)

pg.run()
