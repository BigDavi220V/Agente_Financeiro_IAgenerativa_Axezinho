import streamlit as st
import requests
import pandas as pd
import json
from conteudo import carregar_dados, gerar_contexto_llm
from gamificacao import calcular_progresso_nivel, calcular_progresso_meta

# ============ CONFIGURAÇÃO ============
# URL padrão do Ollama (como no projeto do falvojr)
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "qwen2:0.5b" 

# ============ CARREGAR DADOS ============
perfil, enciclopedia, missoes, cofrinho = carregar_dados()

if perfil is None:
    st.error("🚨 Erro Crítico: Base de dados não encontrada na pasta 'data/'!")
    st.stop()

# ============ SYSTEM PROMPT (PERSONA) ============
# Definido com base no arquivo docs/03-prompts.md
SYSTEM_PROMPT = """
EU SOU O AXÉZINHO 🎒, um guia de aventuras econômicas para crianças.
Sua missão é ensinar educação financeira de forma lúdica e gamificada.

REGRAS DE COMPORTAMENTO:
1. Use a 'ENCICLOPÉDIA' fornecida no contexto para explicar conceitos. Se não souber, diga que é "magia de adulto".
2. Se a criança falar em GASTAR ou COMPRAR, pergunte sempre: "Isso é um DESEJO ou uma NECESSIDADE?".
3. Incentive a completar as MISSÕES para ganhar XP.
4. Use os dados do PERFIL para personalizar (fale o nome, quanto falta pro skate, etc).
5. NUNCA recomende investimentos reais (Bolsa, Cripto). Redirecione para o "Cofrinho".
6. Seja curto, use emojis e fale como um amigo aventureiro.
"""

# ============ FUNÇÃO DE COMUNICAÇÃO COM OLLAMA ============
def perguntar_axezinho(msg_usuario):
    # 1. Gera o contexto atualizado com os dados mais recentes
    contexto_dados = gerar_contexto_llm(perfil, enciclopedia, missoes, cofrinho)
    
    # 2. Monta o prompt final
    prompt_completo = f"""
    {SYSTEM_PROMPT}

    DADOS ATUAIS DO JOGO (Contexto):
    {contexto_dados}

    PERGUNTA DO EXPLORADOR: {msg_usuario}
    """

    try:
        # Chamada à API do Ollama (igual ao exemplo do falvojr)
        payload = {
            "model": MODELO,
            "prompt": prompt_completo,
            "stream": False
        }
        r = requests.post(OLLAMA_URL, json=payload)
        
        if r.status_code == 200:
            return r.json()['response']
        else:
            return f"Ocorreu um erro no meu cérebro digital... (Erro {r.status_code})"
            
    except requests.exceptions.ConnectionError:
        return "🔌 Não consegui conectar ao Ollama! Verifique se ele está rodando com 'ollama serve'."

# ============ INTERFACE (STREAMLIT) ============
st.set_page_config(page_title="Axézinho - Aventura", page_icon="🎒", layout="wide")

# --- SIDEBAR (GAMIFICAÇÃO) ---
with st.sidebar:
    st.image("https://img.freepik.com/vetores-gratis/cofrinho-fofo-com-moeda_1308-133566.jpg?w=200", width=150) # Placeholder
    st.title(f"Explorador {perfil['nome']}")
    st.caption(f"Nível: {perfil['titulo']}")
    
    # Barra de XP
    xp_pct = calcular_progresso_nivel(perfil)
    st.progress(xp_pct)
    st.write(f"XP: {perfil['xp_atual']} / {perfil['xp_proximo_nivel']}")
    
    st.markdown("---")
    st.subheader("🎯 Meta: " + perfil['meta_atual']['nome'])
    
    # Barra da Meta
    meta_pct = calcular_progresso_meta(perfil)
    st.progress(meta_pct)
    
    c1, c2 = st.columns(2)
    c1.metric("Guardado", f"R$ {perfil['meta_atual']['guardado']}")
    c2.metric("Falta", f"R$ {perfil['meta_atual']['custo'] - perfil['meta_atual']['guardado']:.2f}")

# --- ÁREA PRINCIPAL ---
st.title("🎒 Chat com Axézinho")
st.markdown("Converse sobre **missões**, **economia** ou peça ajuda para **juntar moedas**!")

# Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do Usuário
if prompt := st.chat_input("Digite aqui, pequeno gafanhoto..."):
    # Exibe msg usuário
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chama o Ollama
    with st.chat_message("assistant"):
        with st.spinner("Consultando o mapa do tesouro... 🗺️"):
            resposta = perguntar_axezinho(prompt)
            st.markdown(resposta)
    
    # Salva resposta
    st.session_state.messages.append({"role": "assistant", "content": resposta})

# --- ABAS DE DADOS (VISUALIZAÇÃO) ---
# Adicionamos isso para o usuário ver os dados que o LLM está lendo
st.divider()
tab1, tab2 = st.tabs(["📜 Missões Ativas", "💰 Extrato do Cofrinho"])

with tab1:
    for m in missoes:
        status = "✅" if m['status'] == 'concluido' else "⬜"
        st.write(f"**{status} {m['titulo']}** (+{m['xp']} XP): {m['descricao']}")

with tab2:
    st.dataframe(cofrinho, use_container_width=True)