import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestão Clínica - Luma Silva", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #F4EFE5; }
    .patient-card {
        background-color: #ffffff;
        border-left: 10px solid #7D9147;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .patient-name { color: #CF9999; font-size: 26px; font-weight: bold; margin-bottom: 2px; }
    .patient-meta { color: #7D9147; font-size: 14px; margin-bottom: 15px; font-weight: 600; }
    .ai-analysis { 
        background-color: #fdfcf9; 
        border-radius: 10px; 
        padding: 15px; 
        color: #444; 
        line-height: 1.6;
        border: 1px dashed #CF9999;
    }
    .recordatorio-header { color: #7D9147; font-weight: bold; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #CF9999;'>👩‍⚕️ Painel de Consultas - Luma Silva</h1>", unsafe_allow_html=True)

URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVfY6D-nPMeN8GASlk5aH6Q2yclQWH8vYrEgwguYXk50vVnyqkki4Pf3hkY687S1kL7pMtOW-Fq-VM/pub?gid=0&single=true&output=csv"

try:
    
    df = pd.read_csv(URL_PLANILHA)
    df.fillna("Não informado", inplace=True)
    
    busca = st.text_input("🔍 Pesquisar paciente pelo nome:", "").strip().lower()
    
    if busca:
        df_exibir = df[df['Nome'].str.lower().str.contains(busca)]
    else:
        df_exibir = df

    df_exibir = df_exibir.iloc[::-1]

    st.markdown(f"<p style='color: #7D9147;'>Exibindo {len(df_exibir)} registro(s)</p>", unsafe_allow_html=True)

    for index, row in df_exibir.iterrows():
        with st.container():
            st.markdown(f"""
                <div class="patient-card">
                    <div class="patient-name">👤 {row['Nome'].title()}</div>
                    <div class="patient-meta">📧 {row['Email']} &nbsp;&nbsp; | &nbsp;&nbsp; 📞 {row['Telefone']}</div>
                    <div class="ai-analysis">
                        <strong>🧬 Resumo Clínico e Análise de IA:</strong><br>
                        {str(row['Resumo da IA']).replace("**", "<strong>").replace("\n", "<br>")}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Recordatório 24h dentro de um Expander 
            with st.expander("🍎 Ver Recordatório 24h Bruto"):
                if 'Recordatório' in row and row['Recordatório'] != 'Não preenchido':
                    st.markdown(f"""<div class="recordatorio-text">{row['Recordatório']}</div>""", unsafe_allow_html=True)
                else:
                    st.info("O campo de Recordatório será preenchido nos próximos envios do Tally.")

except Exception as e:
    st.error(f"Erro ao conectar com a planilha: {e}")