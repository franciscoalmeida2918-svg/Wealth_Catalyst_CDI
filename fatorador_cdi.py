import streamlit as st
import requests

# 1. Configuração Direta
st.set_page_config(page_title="Wealth Catalyst", layout="centered")
st.title("🛡️ Motor de Fatoração Soberano")

# 2. Busca da Selic Real (Base de Cálculo)
@st.cache_data(ttl=3600)
def buscar_selic():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        return float(requests.get(url).json()[0]['valor'])
    except:
        return 10.75

selic_atual = buscar_selic()
cdi_real = selic_atual - 0.10

# 3. INTERAÇÃO CENTRALIZADA (Onde você digita)
st.subheader("⌨️ Digite os dados do seu título")
col_input1, col_input2 = st.columns(2)

with col_input1:
    pct_digitado = st.number_input("Percentual do CDI (%):", min_value=1.0, value=100.0, step=0.5)

with col_input2:
    tipo_invest = st.selectbox("Tipo de Título:", ["LCI/LCA (Isento)", "CDB (Com IR)"])

# 4. Cálculo de Fatoração Líquida
taxa_ano_bruta = (cdi_real * (pct_digitado / 100))
# Desconto de IR (17.5% para 1 ano) se for CDB
if tipo_invest == "CDB (Com IR)":
    taxa_ano_liq = taxa_ano_bruta * 0.825
else:
    taxa_ano_liq = taxa_ano_bruta

taxa_mes_liq = ((1 + (taxa_ano_liq/100))**(1/12) - 1) * 100

# 5. TABELA ESTILO EXCEL (Foco no Lucro)
st.write("### 📊 Resultado Líquido")
tabela_excel = {
    "Especificação": ["Selic Meta (Hoje)", "CDI Real", f"Seu Título ({pct_digitado}%)"],
    "Taxa Anual (%)": [f"{selic_atual:.2f}%", f"{cdi_real:.2f}%", f"**{taxa_ano_liq:.2f}%**"],
    "Taxa Mensal (%)": ["-", "-", f"**{taxa_mes_liq:.4f}%**"],
    "Lucro Líquido p/ R$ 2.500": ["-", "-", f"**R$ {(2500 * (taxa_mes_liq/100)):.2f}**"]
}
st.table(tabela_excel)

# 6. AVISO CURTO DE TENDÊNCIA
if selic_atual > 10:
    st.warning(f"⚠️ Selic em {selic_atual}%: Títulos Pós-fixados são a melhor estratégia agora.")
else:
    st.info("ℹ️ Selic em queda: Considere travar taxas em títulos Prefixados.")
