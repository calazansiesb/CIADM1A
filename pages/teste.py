import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página principal
st.set_page_config(
    page_title="App de Múltiplas Páginas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Importação das páginas
from pages import page1, page2  # Certifique-se que os arquivos page1.py e page2.py existem na pasta `pages/`

# Menu de navegação
st.sidebar.title("Navegação")
pagina_selecionada = st.sidebar.radio("Selecione a Página", ["Página 1", "Página 2"])

# Redireciona para a página escolhida
if pagina_selecionada == "Página 1":
    page1.app()
elif pagina_selecionada == "Página 2":
    page2.app()
