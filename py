import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Simulador de SN para Tubos Enterrados", layout="centered")

st.title("🔧 Simulador Técnico – SN Recomendado e Deformação de Tubos Enterrados")

# Entradas do usuário via sidebar
st.sidebar.header("Parâmetros de Entrada")

diametro_mm = st.sidebar.number_input(
    "Diâmetro externo do tubo (mm)", min_value=100, max_value=3000, value=1000, step=100)

profundidade_m = st.sidebar.number_input(
    "Profundidade de instalação (m)", min_value=0.5, max_value=10.0, value=2.5, step=0.1)

peso_especifico_solo = st.sidebar.number_input(
    "Peso específico do solo (kN/m³)", min_value=10, max_value=24, value=18)

carga_trafego = st.sidebar.slider(
    "Carga de tráfego (kPa)", min_value=0, max_value=150, value=50)

modulo_reacao = st.sidebar.selectbox(
    "Módulo de reação do solo (E') [MPa]", options=[2, 4, 10, 15])

deformacao_limite = st.sidebar.slider(
    "Deformação admissível (%)", min_value=1, max_value=10, value=5)

# Cálculo do SN mínimo recomendado
carga_total = peso_especifico_solo * profundidade_m + carga_trafego
sn_minimo = (carga_total * (diametro_mm / 1000)) / (modulo_reacao * (deformacao_limite / 100))

# Exibição do resultado
st.markdown(f"### ✅ SN Mínimo Recomendado: **{sn_minimo:.0f} kN/m²**")

# Cálculo de deformações para diferentes SN aplicados
sn_aplicados = np.arange(2000, 16000, 1000)
deformacoes = [(sn, (carga_total * (diametro_mm / 1000)) / (modulo_reacao * sn) * 100) for sn in sn_aplicados]

sns_plot = [d[0] for d in deformacoes]
defs_plot = [d[1] for d in deformacoes]

# Gráfico da deformação
st.subheader("📉 Deformação Real Estimada x SN Aplicado")

fig, ax = plt.subplots()
ax.plot(sns_plot, defs_plot, marker='o', label="Deformação (%)")
ax.axhline(deformacao_limite, color='r', linestyle='--', label='Limite admissível')
ax.set_xlabel("SN Aplicado (kN/m²)")
ax.set_ylabel("Deformação (%)")
ax.grid(True)
ax.legend()
st.pyplot(fig)

