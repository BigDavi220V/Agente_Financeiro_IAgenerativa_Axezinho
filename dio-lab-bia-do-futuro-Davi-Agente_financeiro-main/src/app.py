import streamlit as st
import requests
import pandas as pd
from conteudo import carregar_dados, gerar_contexto_llm
from gamificacao import calcular_progresso_nivel, calcular_progresso_meta

# ============ CONFIGURAÇÃO ============
OLLAMA_URL = "http://localhost:11434/api/generate"
MODELO = "qwen3:1.7b"

#*Alternativas de modelos*
#### Modelo = "qwen3:1.7b"
#### Modelo = "qwen3:0.6b"
#### Modelo = "deepseek-r1:1.5b"
#### Modelo = "llama3.2:latest"
#### Modelo = "llama3.2:1b"
#### Modelo = "gpt-oss"


# ============ CARREGAR DADOS ============
perfil, enciclopedia, missoes, cofrinho, flashcards = carregar_dados()

if perfil is None:
    st.error("🚨 Erro: Verifique se os arquivos JSON e CSV estão na pasta data!")
    st.stop()

# ============ SYSTEM PROMPT (BLINDAGEM) ============
SYSTEM_PROMPT = """
Você é o Axézinho 🎒, mentor financeiro para crianças.
Sua regra número 1 é: NÃO INVENTE. Use apenas os dados fornecidos abaixo.

DIRETRIZES:
1. Se a pergunta estiver nos [FLASHCARDS], responda exatamente como está lá.
2. Se for sobre um conceito (ex: Inflação, Juros, Doação), use o [DICIONÁRIO ECONÔMICO].
3. Se a criança pedir dinheiro, sugira as [MISSÕES] ou o 'Empreendedorismo Mirim'.
4. Sempre verifique 'Desejo vs Necessidade' antes de apoiar uma compra.
5. Fale de forma simples e use emojis.
"""

# ============ FUNÇÃO DE COMUNICAÇÃO COM OLLAMA ============
def perguntar_axezinho(msg_usuario):
    contexto = gerar_contexto_llm(perfil, enciclopedia, missoes, cofrinho, flashcards)
    
    prompt = f"""
    {SYSTEM_PROMPT}
    
    === SEU CONHECIMENTO (DADOS) ===
    {contexto}
    
    === PERGUNTA DA CRIANÇA ===
    "{msg_usuario}"
    
    === SUA RESPOSTA ===
    """

    try:
        # Temperatura 0.2 para evitar 'criatividade' excessiva (fuga do tema)
        r = requests.post(OLLAMA_URL, json={
            "model": MODELO,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.2, "num_ctx": 4096}
        })
        
        if r.status_code == 200:
            return r.json()['response']
        else:
            return f"Erro técnico no Ollama: {r.status_code}"
    except:
        return "O Axézinho está tirando um cochilo... (Ollama desconectado 🔌)"

# ============ INTERFACE (STREAMLIT) ============
st.set_page_config(page_title="Axézinho - Mestre das Moedas", page_icon="🎒", layout="wide")

# --- SIDEBAR (GAMIFICAÇÃO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2953/2953363.png", width=100)
    st.title(f"Explorador {perfil['nome']}")
    st.write(f"**Nível:** {perfil['titulo']}")
    st.progress(calcular_progresso_nivel(perfil))
    
    st.divider()
    st.subheader(f"🎯 Meta: {perfil['meta_atual']['nome']}")
    st.progress(calcular_progresso_meta(perfil))
    falta = perfil['meta_atual']['custo'] - perfil['meta_atual']['guardado']
    st.caption(f"Faltam apenas R$ {falta:.2f}!")

# --- ÁREA PRINCIPAL ---
st.title("🎒 Chat com Axézinho")
st.markdown("Pergunte sobre **dinheiro**, **missões** ou **como realizar sonhos**!")

# Histórico de Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# Input do Usuário
if prompt := st.chat_input("Diga: Quero comprar um doce..."):
    # Exibe msg usuário
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Chama o Ollama
    with st.chat_message("assistant"):
        with st.spinner("Consultando os Flashcards..."):
            resp = perguntar_axezinho(prompt)
            st.write(resp)
    
    # Salva resposta
    st.session_state.messages.append({"role": "assistant", "content": resp})

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