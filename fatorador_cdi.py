import streamlit as st
import requests

# 1. Configuração de Interface Soberana
st.set_page_config(page_title="Wealth Catalyst - Master CDI", layout="wide")
st.title("🛡️ Motor de Fatoração Soberano & Projeção")

# 2. Busca Automática (Base de Comparação)
@st.cache_data(ttl=3600)
def buscar_selic():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        return float(requests.get(url).json()[0]['valor'])
    except:
        return 10.75

selic_oficial = buscar_selic()
cdi_oficial = selic_oficial - 0.10 # Regra de Ouro [cite: 2026-02-26]

# 3. Painel de Interação e Autonomia [cite: 2026-02-27]
st.sidebar.header("🎛️ Painel de Controle")
pct_cdi = st.sidebar.number_input("Digite o % do CDI do seu título (Ex: 110):", min_value=1.0, value=100.0, step=0.5)
isento = st.sidebar.checkbox("Título Isento (LCI/LCA)?", value=True)

# 4. Cálculo de Fatoração em Tempo Real [cite: 2026-02-27]
taxa_ano_bruta = (cdi_oficial * (pct_cdi / 100))
taxa_mes_bruta = ((1 + (taxa_ano_bruta/100))**(1/12) - 1) * 100

# Cálculo Líquido (IR de 17.5% para prazos de 1 ano se não for isento) [cite: 2025-02-25]
taxa_ano_liq = taxa_ano_bruta if isento else taxa_ano_bruta * 0.825
taxa_mes_liq = ((1 + (taxa_ano_liq/100))**(1/12) - 1) * 100

# 5. Exibição de Resultados (Excel Style Table) [cite: 2026-02-27]
st.subheader("📊 Resultados da Fatoração Líquida")
st.table({
    "Indicador": ["Taxa Selic Meta (BCB)", "CDI Real (Mercado)", f"Seu Título ({pct_cdi}% do CDI)"],
    "Taxa Anual (%)": [f"{selic_oficial:.2f}%", f"{cdi_oficial:.2f}%", f"{taxa_ano_liq:.2f}%"],
    "Taxa Mensal (%)": ["-", "-", f"{taxa_mes_liq:.4f}%"],
    "Status": ["Oficial", "Base Bancária", "LÍQUIDO REAL"]
})

# 6. Avisos e Projeções Estratégicas [cite: 2026-02-26]
st.divider()
st.subheader("⚠️ Avisos de Mercado & Tendência")

if selic_oficial >= 10.0:
    st.warning(f"**ALERTA DE ALTA:** Selic em {selic_oficial}%. O cenário favorece manter aportes de R$ 2.500,00 em títulos pós-fixados (LCI/LCA) para maximizar o ganho de capital rápido. [cite: 2026-02-27]")
else:
    st.info("**ALERTA DE QUEDA:** Tendência de redução. Considere avaliar títulos prefixados para travar a rentabilidade atual antes da próxima reunião do Copom. [cite: 2026-02-26]")

st.info(f"💡 **ESTRATÉGIA:** Para seu aporte de **R$ 2.500,00**, esse título rende **R$ {(2500 * (taxa_mes_liq/100)):.2f} líquidos** no primeiro mês. [cite: 2026-02-27]")
