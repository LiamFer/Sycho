import streamlit as st
import pandas as pd
import datetime
import numpy as np
import os

if "selectedFood" not in st.session_state:
    st.session_state.selectedFood = []

if "options" not in st.session_state:
    st.session_state.options = []

# Puxando o Arquivo com as Infos
FILEPATH = r"C:\\Users\\Windows\\Desktop\\cc.xlsx"


def getFile():
    return pd.read_excel(FILEPATH)


if os.path.isfile(FILEPATH):
    df = getFile()
else:
    data = {
        "Data e Horário": [],
        "Refeição": [],
        "Compulsão": [],
        "Quantidade": [],
        "Alimentos Consumidos": [],
        "Situação": [],
    }
    df = pd.DataFrame(data)
    df.to_excel(FILEPATH, index=False)
    df = getFile()


st.markdown(
    f'<h1 style="background-color:#9fb851;color:#ffffff;font-size:44px;border-radius:10px;padding:10px;margin-bottom:20px">{"Diário"}</h1>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.write("Inside the form")

    col1, col2, col3 = st.columns(3)

    with col1:
        dateTime = st.date_input("Data e Horário", datetime.date(2019, 7, 6))
        compulsao = st.radio(
            "Houve Compulsão",
            ["Sim", "Não"],
        )

    with col2:
        refeicao = st.selectbox(
            "Refeição",
            ("Café da Manhã", "Almoço", "Janta"),
        )
        quantityConsumed = st.number_input("Quantidade Consumida (KG)")

    with col3:
        inputFood = st.text_input("Adicione um Alimento", "")

        if inputFood:
            if inputFood not in st.session_state.options:
                st.session_state.options.append(inputFood)
                st.session_state.selectedFood.append(inputFood)
            inputFood = ""

        foodOptions = st.multiselect(
            "Alimentos Consumidos",
            st.session_state.options,
            st.session_state.selectedFood,
        )
        

    situation = st.selectbox(
        "Situação: O que estava acontecendo?",
        ("Email", "Home phone", "Mobile phone"),
    )
    
    submitButton = st.button("Submit")

    if submitButton:
        new_row = {
            "Data e Horário": dateTime,
            "Refeição": refeicao,
            "Compulsão": compulsao,
            "Quantidade": quantityConsumed,
            "Alimentos Consumidos": ",".join(st.session_state.selectedFood),
            "Situação": situation
        }
        
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
        df.to_excel(FILEPATH, index=False)
        st.success("Row appended successfully!")
        
