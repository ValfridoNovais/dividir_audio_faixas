import streamlit as st
from datetime import datetime, timedelta

# Configurações iniciais
st.title("Simulador Tesouro Prefixado 2035")
st.subheader("Evolução dos Investimentos e Projeções de Retirada")

# Dados do título
valor_cota = 7.62
rentabilidade_anual = 15.05 / 100  # Rentabilidade anual
vencimento = datetime(2035, 1, 1).date()  # Converte para date
dias_ano = 252  # Base de dias úteis

# Entrada de dados
valor_investido = st.number_input("Investimento Inicial (R$):", min_value=0.0, value=1000.0)
aporte_mensal = st.number_input("Aporte Mensal (R$):", min_value=0.0, value=100.0)
data_resgate = st.date_input("Escolha uma data de resgate:", min_value=datetime.today().date(), value=vencimento)

# Rentabilidade diária
rentabilidade_diaria = (1 + rentabilidade_anual) ** (1 / dias_ano) - 1

# Cálculo de evolução com aportes mensais
def calcular_investimento_mensal(valor_inicial, aporte, data_final, data_resgate, rent_diaria):
    total_acumulado = valor_inicial * ((1 + rent_diaria) ** ((data_resgate - datetime.today().date()).days))
    data_atual = datetime.today().date()
    total_aportes = 0  # Para calcular o total investido
    while data_atual < data_resgate:
        dias_restantes = (data_resgate - data_atual).days
        total_acumulado += aporte * ((1 + rent_diaria) ** dias_restantes)
        total_aportes += aporte
        data_atual += timedelta(days=30)  # Incremento de 1 mês
    return total_acumulado, total_aportes

# Resultado final com aportes
valor_final_vencimento, total_aportes_vencimento = calcular_investimento_mensal(
    valor_inicial=valor_investido,
    aporte=aporte_mensal,
    data_final=vencimento,
    data_resgate=vencimento,
    rent_diaria=rentabilidade_diaria
)

valor_resgate, total_aportes_resgate = calcular_investimento_mensal(
    valor_inicial=valor_investido,
    aporte=aporte_mensal,
    data_final=vencimento,
    data_resgate=data_resgate,
    rent_diaria=rentabilidade_diaria
)

# Tributação
def calcular_ir(valor, valor_inicial, dias):
    lucro = valor - valor_inicial
    if dias <= 180:
        aliquota = 0.225
    elif dias <= 360:
        aliquota = 0.20
    elif dias <= 720:
        aliquota = 0.175
    else:
        aliquota = 0.15
    return lucro * aliquota

# IR no vencimento e na data de resgate
ir_vencimento = calcular_ir(
    valor=valor_final_vencimento,
    valor_inicial=valor_investido + total_aportes_vencimento,
    dias=(vencimento - datetime.today().date()).days
)

ir_resgate = calcular_ir(
    valor=valor_resgate,
    valor_inicial=valor_investido + total_aportes_resgate,
    dias=(data_resgate - datetime.today().date()).days
)

# Total investido
total_investido_vencimento = valor_investido + total_aportes_vencimento
total_investido_resgate = valor_investido + total_aportes_resgate

# Exibição dos resultados com frame estilizado
with st.container():
    st.markdown("### Resultado da Simulação:")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 15px; border-radius: 10px; border: 1px solid #ddd;">
        <h4>📊 No Vencimento (01/01/2035):</h4>
        <ul>
            <li><b>Total Investido:</b> R${:,.2f}</li>
            <li><b>Valor Bruto:</b> R${:,.2f}</li>
            <li><b>IR:</b> R${:,.2f}</li>
            <li><b>Valor Líquido:</b> R${:,.2f}</li>
        </ul>
        <h4>📅 Na Data Escolhida ({:%d/%m/%Y}):</h4>
        <ul>
            <li><b>Total Investido:</b> R${:,.2f}</li>
            <li><b>Valor Bruto:</b> R${:,.2f}</li>
            <li><b>IR:</b> R${:,.2f}</li>
            <li><b>Valor Líquido:</b> R${:,.2f}</li>
        </ul>
    </div>
    """.format(
        total_investido_vencimento, valor_final_vencimento, ir_vencimento, valor_final_vencimento - ir_vencimento,
        data_resgate, total_investido_resgate, valor_resgate, ir_resgate, valor_resgate - ir_resgate
    ), unsafe_allow_html=True)
