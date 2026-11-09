import streamlit as st
import pandas as pd

# ---------- Passos 4, 6 e 7: Olá, mundo + variáveis ----------
nome = "Nicolas Faria" 
idade = 18        
st.write("Olá, mundo")
st.write(f"Meu nome é {nome} e eu tenho {idade} anos.")

# ---------- Passos 11 e 12: título e subtítulo ----------
st.title("Meu primeiro dash")
st.subheader(nome)

# ---------- Passos 10 e 13: dataframe ----------
df = pd.DataFrame({
    "Matéria": ["Português", "Matemática", "Python", "Frame"],
    "Nota": [5, 9, 7, 10]
})
st.write(df)

# ---------- Passos 16 e 17: supermercado ----------
st.header("Supermercado")

precos = {
    "Arroz": 25.90,
    "Feijão": 8.50,
    "Leite": 5.20,
    "Pão": 7.80,
    "Café": 18.90,
    "Ovos (dúzia)": 12.00,
}


def calcular_compra(itens_escolhidos):
    """Soma o preço dos itens escolhidos."""
    return sum(precos[item] for item in itens_escolhidos)


escolhidos = st.multiselect("Escolha os itens da sua compra:", list(precos.keys()))

if escolhidos:
    total = calcular_compra(escolhidos)
    st.table(pd.DataFrame({
        "Item": escolhidos,
        "Preço (R$)": [precos[i] for i in escolhidos],
    }))
    st.write(f"**Total da compra: R$ {total:.2f}**")
else:
    st.write("Nenhum item selecionado.")