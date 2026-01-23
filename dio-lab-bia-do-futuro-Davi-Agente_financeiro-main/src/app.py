import streamlit as st
import pandas as pd
import random
from conteudo import carregar_dados, buscar_conceito
from gamificacao import calcular_nivel

# ============ CONFIGURAÇÃO INICIAL ============
st.set_page_config(page_title="Axézinho - Aventura Econômica", page_icon="🎒")

# ============ CARREGAMENTO DE DADOS ============
perfil, enciclopedia, missoes, cofrinho = carregar_dados()

if perfil is None:
    st.error("🚨 Erro: Não encontrei os arquivos na pasta 'data'. Verifique se eles existem!")
    st.stop()

# ============ CÉREBRO DO AXÉZINHO (SEM OLLAMA) ============
def responder_local(msg):
    msg = msg.lower()
    
    # 1. Perguntas sobre COMPRAR ou GASTAR
    if any(x in msg for x in ["comprar", "gastar", "quero", "preço"]):
        saldo_meta = perfil['meta_atual']['custo'] - perfil['meta_atual']['guardado']
        respostas = [
            f"Calma lá, explorador! 🛑 Antes de abrir a carteira, me diga: isso é um **DESEJO** ou uma **NECESSIDADE**?",
            f"Hmm... comprar é legal, mas você lembra da sua meta? Ainda faltam R$ {saldo_meta:.2f} para o seu {perfil['meta_atual']['nome']}. Será que vale a pena gastar agora?",
            "Opa! Vamos usar a regra dos 5 Rs? Será que dá pra **REUTILIZAR** algo que você já tem em vez de comprar?"
        ]
        return random.choice(respostas)

    # 2. Perguntas sobre CONCEITOS (busca na enciclopédia)
    conceito_encontrado = buscar_conceito(msg, enciclopedia)
    if conceito_encontrado:
        return conceito_encontrado

    # 3. Perguntas sobre META ou SONHO
    if any(x in msg for x in ["meta", "sonho", "skate", "bicicleta", "quanto falta"]):
        falta = perfil['meta_atual']['custo'] - perfil['meta_atual']['guardado']
        return f"🎯 Estamos de olho no prêmio! Sua meta é **{perfil['meta_atual']['nome']}**.\n\nVocê já guardou **R$ {perfil['meta_atual']['guardado']:.2f}** e faltam apenas **R$ {falta:.2f}**. Se você fizer uma missão hoje, a gente chega lá mais rápido!"

    # 4. Perguntas sobre GANHAR DINHEIRO ou MISSÃO
    if any(x in msg for x in ["ganhar", "dinheiro", "missão", "trabalho"]):
        return "Quer moedas? 🪙 Então mãos à obra! Dê uma olhada na aba **'Pergaminho de Missões'**. Se você completar o desafio 'O Negociador', ganha XP e entende como o escambo funciona!"

    # 5. Saudações
    if any(x in msg for x in ["oi", "olá", "ola", "bom dia", "boa tarde"]):
        return f"Olá, {perfil['nome']}! 🖖 Eu sou o Axézinho. Estou pronto para proteger suas moedas! O que vamos aprender hoje?"

    # 6. Resposta Padrão (Fallback)
    return "Eita, ainda estou aprendendo essa palavra! 🤯 Tente perguntar sobre 'comprar', 'minha meta' ou 'escambo'. Ou veja suas missões!"

# ============ INTERFACE GRÁFICA ============

# --- BARRA LATERAL (PERFIL) ---
with st.sidebar:
    st.title(f"{perfil['avatar']} Perfil")
    st.write(f"**Explorador:** {perfil['nome']}")
    st.write(f"**Nível:** {perfil['titulo']}")
    
    # Barra de XP com cor personalizada
    xp_pct = calcular_nivel(perfil)
    st.progress(xp_pct)
    st.caption(f"XP: {perfil['xp_atual']} / {perfil['xp_proximo_nivel']}")
    
    st.markdown("---")
    st.subheader("🏆 Meta Atual")
    st.info(f"{perfil['meta_atual']['nome']}")
    col1, col2 = st.columns(2)
    col1.metric("Guardado", f"R$ {perfil['meta_atual']['guardado']}")
    col2.metric("Meta", f"R$ {perfil['meta_atual']['custo']}")

# --- ÁREA PRINCIPAL ---
st.title("🎒 Axézinho: Jornada Econômica")

# Abas para organizar a tela
tab_chat, tab_missoes, tab_cofre = st.tabs(["💬 Conversar com Axézinho", "📜 Pergaminho de Missões", "💰 Cofrinho Virtual"])

# ABA 1: CHAT
with tab_chat:
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 10px; border-radius: 10px; margin-bottom: 20px;'>
        👋 Oi! Eu sou seu guia. Pergunte coisas como: 
        <b>"O que é escambo?"</b>, <b>"Quero comprar um doce"</b> ou <b>"Quanto falta pra minha meta?"</b>
    </div>
    """, unsafe_allow_html=True)

    # Histórico de mensagens na sessão
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mostra mensagens antigas
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Campo de entrada
    if prompt := st.chat_input("Digite sua dúvida aqui..."):
        # Mostra pergunta do usuário
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Axézinho responde (Simulação local)
        with st.chat_message("assistant"):
            with st.spinner("Consultando meu diário..."):
                resposta = responder_local(prompt)
                st.markdown(resposta)
        st.session_state.messages.append({"role": "assistant", "content": resposta})

# ABA 2: MISSÕES
with tab_missoes:
    st.header("Missões Disponíveis")
    st.write("Complete tarefas para ganhar XP e subir de nível!")
    
    for missao in missoes:
        with st.container():
            col_a, col_b = st.columns([0.1, 0.9])
            concluida = (missao.get('status') == 'concluido')
            
            with col_a:
                st.checkbox("Done", value=concluida, key=f"chk_{missao['id']}", disabled=True)
            with col_b:
                st.subheader(f"{missao['titulo']} (+{missao['xp']} XP)")
                st.write(missao['descricao'])
                if concluida:
                    st.success("Completada! 🎉")
                else:
                    st.info("Em andamento...")
            st.divider()

# ABA 3: COFRE
with tab_cofre:
    st.header("Seu Diário Financeiro")
    
    # Métricas rápidas
    total_entrada = cofrinho[cofrinho['tipo'] == 'ganho']['valor'].sum()
    total_saida = cofrinho[cofrinho['tipo'] == 'gasto']['valor'].sum()
    saldo = total_entrada - total_saida
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Ganhei", f"R$ {total_entrada:.2f}", delta_color="normal")
    c2.metric("Gastei", f"R$ {total_saida:.2f}", delta_color="inverse")
    c3.metric("Saldo Atual", f"R$ {saldo:.2f}")
    
    st.subheader("Histórico")
    # Estilizando a tabela
    def cor_tipo(val):
        color = '#d4edda' if val == 'ganho' else '#f8d7da'
        return f'background-color: {color}'

    st.dataframe(
        cofrinho.style.applymap(cor_tipo, subset=['tipo']),
        use_container_width=True
    )