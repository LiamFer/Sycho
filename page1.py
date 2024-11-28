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

user_home = os.path.expanduser("~")  # Obtém o diretório home do usuário
FILEPATH = os.path.join(user_home, "Desktop", "diarioAlimentar.xlsx")

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
        

    situation = st.text_input(
        "Situação: O que estava acontecendo?",
        label_visibility = "visible",
        disabled = False,
        placeholder= "Descreva o que estava acontecendo no momento",
    )

    beforeSituation = st.text_input(
        "Como me senti antes?",
        label_visibility = "visible",
        disabled = False,
        placeholder= "Descreva o que estava sentindo antes da refeição",
    )
    
    duringSituation = st.text_input(
        "Como me senti durante?",
        label_visibility = "visible",
        disabled = False,
        placeholder= "Descreva o que estava sentindo durante a refeição",
    )

    afterSituation = st.text_input(
        "Como me senti depois?",
        label_visibility = "visible",
        disabled = False,
        placeholder= "Descreva o que estava sentindo após a refeição",
    )

    
    
    submitButton = st.button("Submit")

    

    if submitButton:
        new_row = {
            "Data e Horário": dateTime,
            "Refeição": refeicao,
            "Compulsão": compulsao,
            "Quantidade": quantityConsumed,
            "Alimentos Consumidos": ",".join(st.session_state.selectedFood),
            "Situação": situation,
            "Como eu estava me sentindo antes?": beforeSituation,
            "Como me senti depois?": afterSituation,
            "Como me senti durante?": duringSituation
        }
        
        new_row_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_row_df], ignore_index=True)
        df.to_excel(FILEPATH, index=False)
        st.success("Row appended successfully!")
        
