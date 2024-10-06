import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go

st.set_page_config(layout="wide")


def page2():
    # Puxando o Arquivo com as Infos
    FILEPATH = r"C:\\Users\\Windows\\Desktop\\cc.xlsx"
    df = pd.read_excel(FILEPATH)

    col1, col2 = st.columns(2)

    with col1:
        st.dataframe(df)


    # Puxando os Alimentos mais consumidos pela Pessoa
    food = {
        "Alimentos": [k for i in df["Alimentos Consumidos"].str.split(",").to_numpy() for k in i] ,
    }
    food = pd.DataFrame(food)
    mostConsumedItems = food.groupby("Alimentos")["Alimentos"].count().reset_index(name='count').sort_values(['count'], ascending=False).head(3).to_numpy()

    with col2:
        col1, col2, col3 = st.columns(3)
        col1.metric("O Mais Consumido", mostConsumedItems[0][0], f'{mostConsumedItems[0][1]} Vezes', delta_color="off")
        col2.metric("Segundo mais Consumido", mostConsumedItems[1][0], f'{mostConsumedItems[1][1]} Vezes', delta_color="off")
        col3.metric("Terceiro mais Consumido", mostConsumedItems[2][0], f'{mostConsumedItems[2][1]} Vezes', delta_color="off")

    def create_plotly_graph(data):
        x_values = df["Data e Horário"]
        y_values = df["Quantidade"]
        print(y_values)
        colors = ["red" if y < 10 else "green" for y in y_values]

        fig = go.Figure(
            data=go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                marker=dict(size=12, color=colors),
                line=dict(color="gray"),  # Adjust line color as needed
            )
        )

        fig.update_layout(
            title="QTD de Comida Consumida",  # Replace with your desired title
            xaxis_title="Data",  # Replace with your desired label
            yaxis_title="Quantidade (KG)",  # Replace with your desired label
        )

        return fig

    fig = create_plotly_graph(df)
    st.plotly_chart(fig)


with st.sidebar:
    st.logo("marcho_sister.png")
    pg = st.navigation(
        [
            st.Page("page1.py", title="Overview", icon="🔥"),
            st.Page(page2, title="Second page", icon=":material/favorite:"),
        ]
    )

pg.run()
