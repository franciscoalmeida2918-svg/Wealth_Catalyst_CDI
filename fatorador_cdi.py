import requests
from datetime import datetime

def buscar_selic_real():
    """Busca a Meta Selic atual via API do Banco Central"""
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
        resposta = requests.get(url, timeout=10)
        selic = float(resposta.json()[0]['valor'])
        return selic
    except:
        return 10.75 # Valor padrão de segurança

def calcular_fatoracao():
    print(f"--- MOTOR DE FATORAÇÃO SOBERANO ({datetime.now().strftime('%d/%m/%Y')}) ---")
    
    # 1. Dados do Mercado em Tempo Real [cite: 2026-02-26]
    selic = buscar_selic_real()
    cdi = selic - 0.10 # Diferença real praticada pelos bancos
    
    print(f"Taxa Selic Atual: {selic:.2f}% a.a.")
    print(f"Taxa CDI Real: {cdi:.2f}% a.a.")
    print("-" * 45)

    # 2. Entrada de Autonomia [cite: 2026-02-27]
    pct_titulo = float(input("Digite o % do CDI do seu título (Ex: 90 ou 110): "))

    # 3. Fatoração Matemática [cite: 2026-02-27]
    taxa_ano = (cdi * (pct_titulo / 100))
    taxa_mes = ((1 + (taxa_ano/100))**(1/12) - 1) * 100

    print(f"\n--- RESULTADO DA CONVERSÃO ---")
    print(f"Para um título de {pct_titulo}% do CDI:")
    print(f">> Taxa Anual Real (a.a.): {taxa_ano:.2f}%")
    print(f">> Taxa Mensal Real (a.m.): {taxa_mes:.4f}%")

if __name__ == "__main__":
    calcular_fatoracao()
