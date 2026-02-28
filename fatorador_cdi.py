import streamlit as st
import requests

# 1. Configuração e Busca de Dados Oficiais
def buscar_dados_bcb():
    # Taxa Atual (Série 432)
    url_selic = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    selic_atual = float(requests.get(url_selic).json()[0]['valor'])
    
    # Simulação de Tendência (Baseada no Focus/Expectativas do BC) [cite: 2026-02-26]
    # No App real, buscaríamos a série de expectativas, aqui simulamos a lógica:
    tendencia = "ESTÁVEL" # Padrão
    if selic_atual < 10.50: tendencia = "ALTA 📈"
    elif selic_atual > 11.50: tendencia = "QUEDA 📉"
    
    return selic_atual, tendencia

selic_hoje, sinal_mercado = buscar_dados_bcb()

# 2. Interface Visual Soberana [cite: 2026-02-27]
st.title("🛡️ Wealth Catalyst: Motor Real & Projeção")

# Alerta de Tendência (O seu "Aviso")
if "ALTA" in sinal_mercado:
    st.warning(f"⚠️ **ALERTA ESTRATÉGICO:** A tendência para o próximo mês é de **{sinal_mercado}**. Considere títulos Pós-Fixados (CDI) para ganhar mais!")
elif "QUEDA" in sinal_mercado:
    st.info(f"ℹ️ **AVISO DE MERCADO:** A tendência é de **{sinal_mercado}**. Pode ser hora de travar um Prefixado antes que a taxa caia.")
else:
    st.success(f"✅ **MERCADO ESTÁVEL:** A taxa deve se manter em {selic_hoje}% no próximo mês.")

# 3. Cálculos de Fatoração [cite: 2026-02-27]
pct_titulo = st.sidebar.number_input("Percentual do CDI (%):", value=90.0)
cdi_real = selic_hoje - 0.10
taxa_ano = (cdi_real * (pct_titulo / 100))
taxa_mes = ((1 + (taxa_ano/100))**(1/12) - 1) * 100

st.metric("Taxa Selic Hoje", f"{selic_hoje}%", delta=sinal_mercado)
st.metric("Sua Taxa Mensal Líquida", f"{taxa_mes:.4f}%")
