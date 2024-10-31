import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import datetime

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

    with st.container():
        # Puxando os Alimentos mais consumidos pela Pessoa
        food = {
            "Alimentos": [
                k.strip().title()
                for i in df["Alimentos Consumidos"].str.split(",").to_numpy()
                for k in i
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
        st.markdown(
            f'<h1 style="background-color:#9fb851;color:#ffffff;font-size:44px;border-radius:10px;padding:10px">{"Overview"}</h1>',
            unsafe_allow_html=True,
        )
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

    st.divider()

    with st.container():
        col1, col2 = st.columns(2)

        with col1:
            fig = create_plotly_graph(df)
            st.plotly_chart(fig)

        with col2:
            st.header("WordCloud")

            with st.container():
                col1, col2, col3 = st.columns(3)

                with col1:
                    compulsao = st.selectbox("Houve Compulsão", ("Todos", "Sim", "Não"))
                    compulsaoValue = compulsao if compulsao != "Todos" else ""
                with col2:
                    periodo = st.multiselect(
                        "Período",
                        ["Antes", "Durante", "Depois"],
                        ["Antes", "Durante", "Depois"],
                    )
                    lookupDict = {
                        "Durante": "Como me senti durante?",
                        "Antes": "Como eu estava me sentindo antes?",
                        "Depois": "Como me senti depois?",
                    }
                with col3:
                    dateFilter = st.date_input(
                        "Escolha a Data",
                        (min(df["Data e Horário"].dt.date), max(df["Data e Horário"].dt.date)),
                        format="DD/MM/YYYY",
                    )
                    beginDate = dateFilter[0]
                    endDate = dateFilter[1]

            tableQuery = "Compulsão.str.contains(@compulsaoValue) & (`Data e Horário`.dt.date >= @beginDate & `Data e Horário`.dt.date <= @endDate)"
            try:
                text = ",".join(
                    [
                        x.strip()
                        for j in [
                            k.split(",")
                            for i in df.query(tableQuery)[
                                [lookupDict[k] for k in periodo]
                            ].to_numpy()
                            for k in i
                        ]
                        for x in j
                    ]
                )
                wordcloud = WordCloud(
                    colormap="gist_earth_r",
                    background_color="#f0f0f0",
                    width=590,
                    height=290,
                ).generate(text)
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            except:
                st.error("Selecione ao menos uma Opção", icon="🚨")

st.markdown(
    """
<style>

    [data-testid=stSidebarContent] {
        background-color: #436d2e;
    }
    
    [data-testid=stSidebarContent] span{
        color: #ffffff
    }
    
    [data-testid=stSidebarContent] header{
        color: #ffffff;
        font-size:30px
    }
    
</style>
""",
    unsafe_allow_html=True,
)

pg = st.navigation(
    {
        "Escolha uma Opção": [
            st.Page(page2, title="Overview", icon="📌"),
            st.Page("page1.py", title="Diário", icon="📝"),
        ]
    }
)


pg.run()
