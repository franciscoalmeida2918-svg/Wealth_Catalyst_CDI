import streamlit as st
import requests

# 1. Configuração de Interface Soberana
st.set_page_config(page_title="Wealth Catalyst - Master CDI", layout="wide")
st.title("🛡️ Motor de Fatoração Soberano")

# 2. Busca Automática da Base (Selic BCB)
@st.cache_data(ttl=3600)
def buscar_selic():
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        return float(requests.get(url).json()[0]['valor'])
    except:
        return 10.75 # Backup caso a API falhe

selic_oficial = buscar_selic()
cdi_oficial = selic_oficial - 0.10 # Regra de Ouro [cite: 2026-02-26]

# 3. INTERAÇÃO: Onde você digita o CDI [cite: 2026-02-27]
st.sidebar.header("📥 Entrada de Dados")
# Aqui é onde você digita o valor, ex: 90, 100, 110
pct_cdi_digitado = st.sidebar.number_input("Digite o % do CDI do Título:", min_value=1.0, value=100.0, step=1.0)
isento_ir = st.sidebar.checkbox("Título Isento (LCI/LCA)?", value=True)

# 4. Cálculos de Fatoração Líquida [cite: 2025-02-25, 2026-02-27]
taxa_ano_bruta = (cdi_oficial * (pct_cdi_digitado / 100))
# IR de 17.5% se não for isento (regra de 1 ano)
taxa_ano_liq = taxa_ano_bruta if isento_ir else taxa_ano_bruta * 0.825
taxa_mes_liq = ((1 + (taxa_ano_liq/100))**(1/12) - 1) * 100

# 5. Tabela Estilo Excel (Foco em Ganho Líquido) [cite: 2026-02-27]
st.subheader(f"📊 Análise do Título: {pct_cdi_digitado}% do CDI")
dados_tabela = {
    "Descrição": ["Selic Atual (BCB)", "CDI Real (Base)", f"Título Digitado ({pct_cdi_digitado}%)"],
    "Taxa Anual Líquida": [f"{selic_oficial:.2f}%", f"{cdi_oficial:.2f}%", f"**{taxa_ano_liq:.2f}%**"],
    "Taxa Mensal Líquida": ["-", "-", f"**{taxa_mes_liq:.4f}%**"],
    "Lucro p/ R$ 2.500 (Mês)": ["-", "-", f"R$ {(2500 * (taxa_mes_liq/100)):.2f}"]
}
st.table(dados_tabela)

# 6. Avisos de Estratégia e Tendência [cite: 2026-02-26]
st.divider()
if selic_oficial >= 10.0:
    st.warning(f"⚠️ **AVISO SOBERANO:** Selic alta ({selic_oficial}%). Foque em bater a inflação com este título de {pct_cdi_digitado}% do CDI. [cite: 2026-02-27]")
else:
    st.info("ℹ️ **ESTRATÉGIA:** Taxas em queda. Considere travar este rendimento se for um Prefixado. [cite: 2026-02-26]")

st.success(f"🎯 **Meta de 10 Anos:** Com aporte de R$ 2.500, este título rende R$ {(2500 * (taxa_mes_liq/100) * 12):.2f} líquidos no primeiro ano. [cite: 2026-02-27]")
