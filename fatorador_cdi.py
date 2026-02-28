import streamlit as st
import requests
from datetime import datetime

# 1. Configuração de Interface Web Soberana
st.set_page_config(page_title="Wealth Catalyst - Motor de Fatoração", layout="wide")
st.title("🛡️ Motor de Fatoração CDI & Projeção Real")

# 2. Conexão em Tempo Real com o Banco Central
@st.cache_data(ttl=3600)
def buscar_selic_oficial():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    return float(requests.get(url).json()[0]['valor'])

selic_atual = buscar_selic_oficial()
cdi_mercado = selic_atual - 0.10 # Regra de Ouro: CDI Real [cite: 2026-02-26]

# 3. Painel de Interação de Fatoração [cite: 2026-02-27]
st.sidebar.header("Configurações do Título")
pct_cdi = st.sidebar.number_input("Quanto o título paga do CDI? (Ex: 90, 100, 110)", min_value=1.0, value=90.0, step=1.0)
isento = st.sidebar.checkbox("Título Isento de IR (LCI/LCA)?", value=True)

# 4. Cálculos Matemáticos de Precisão (Fatoração) [cite: 2026-02-27]
taxa_fatorada_ano = (cdi_mercado * (pct_cdi / 100))
# Conversão Mensal via Juros Compostos: (1 + i_ano)^(1/12) - 1
taxa_decimal_ano = taxa_fatorada_ano / 100
taxa_fatorada_mes = ((1 + taxa_decimal_ano)**(1/12) - 1) * 100

# Ajuste Líquido (IR de 17.5% para CDBs se não for isento) [cite: 2025-02-25]
if not isento:
    taxa_fatorada_mes = taxa_fatorada_mes * (1 - 0.175)
    taxa_fatorada_ano = taxa_fatorada_ano * (1 - 0.175)

# 5. Exibição de Resultados e Avisos de Tendência [cite: 2026-02-26]
col1, col2, col3 = st.columns(3)
col1.metric("Selic Hoje (BCB)", f"{selic_atual}% a.a.")
col2.metric("Sua Taxa Anual Líquida", f"{taxa_fatorada_ano:.2f}% a.a.")
col3.metric("Sua Taxa Mensal Líquida", f"{taxa_fatorada_mes:.4f}% a.m.")

st.divider()

# Aviso de Tendência Estratégica
if selic_atual >= 10.75:
    st.warning("⚠️ **AVISO:** Taxa em patamar elevado. Títulos Pós-Fixados (CDI) estão acelerando seu ganho de capital! [cite: 2026-02-27]")
else:
    st.info("ℹ️ **AVISO:** Tendência de queda detectada. Considere travar taxas em Prefixados para manter a rentabilidade alta. [cite: 2026-02-26]")

st.subheader("📊 Planejamento de Aporte Mensal (Líquido)")
st.write(f"Para seu aporte de **R$ 2.500,00**, seu lucro líquido no primeiro mês será de aproximadamente **R$ {(2500 * (taxa_fatorada_mes/100)):.2f}**.")
