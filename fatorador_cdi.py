import streamlit as st
import requests

# 1. Configuração da Página Web
st.set_page_config(page_title="Wealth Catalyst - Fatorador CDI", layout="centered")
st.title("🛡️ Motor de Fatoração Soberano")

# 2. Busca da Selic em Tempo Real
@st.cache_data(ttl=3600) # Atualiza a cada hora
def buscar_selic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    return float(requests.get(url).json()[0]['valor'])

selic_hoje = buscar_selic()
cdi_real = selic_hoje - 0.10 # Regra de Ouro [cite: 2026-02-26]

st.metric("Taxa Selic (Mercado)", f"{selic_hoje}% a.a.")
st.write(f"**CDI Real (Bancos):** {cdi_real:.2f}% a.a.")

# 3. Interface de Autonomia [cite: 2026-02-27]
pct_titulo = st.number_input("Digite o % do CDI do título (Ex: 90):", min_value=1.0, value=90.0)

# 4. Cálculos e Resultado Líquido
taxa_ano = (cdi_real * (pct_titulo / 100))
taxa_mes = ((1 + (taxa_ano/100))**(1/12) - 1) * 100

st.divider()
st.subheader("Resultado da Fatoração")
col1, col2 = st.columns(2)
col1.metric("Taxa Anual", f"{taxa_ano:.2f}% a.a.")
col2.metric("Taxa Mensal", f"{taxa_mes:.4f}% a.m.")
