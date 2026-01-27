import json
import pandas as pd
import os

def carregar_dados():
    """
    Carrega os arquivos da base de conhecimento do Axézinho.
    """
    try:
        # Ajuste de caminho para garantir que encontre a pasta data
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        perfil = json.load(open(os.path.join(base_path, 'perfil_explorador.json'), encoding='utf-8'))
        enciclopedia = json.load(open(os.path.join(base_path, 'enciclopedia_economia.json'), encoding='utf-8'))
        missoes = json.load(open(os.path.join(base_path, 'missoes.json'), encoding='utf-8'))
        
        csv_path = os.path.join(base_path, 'cofrinho_virtual.csv')
        if os.path.exists(csv_path):
            cofrinho = pd.read_csv(csv_path)
        else:
            cofrinho = pd.DataFrame(columns=['data', 'descricao', 'tipo', 'valor', 'categoria'])
            
        return perfil, enciclopedia, missoes, cofrinho
    except FileNotFoundError as e:
        print(f"Erro ao carregar dados: {e}")
        return None, None, None, None

def gerar_contexto_llm(perfil, enciclopedia, missoes, cofrinho):
    """
    Transforma os dados JSON/CSV em um texto legível para o Ollama.
    """
    
    # Calcula saldo e falta para meta
    total_guardado = perfil['meta_atual']['guardado']
    meta_valor = perfil['meta_atual']['custo']
    falta = meta_valor - total_guardado
    
    contexto = f"""
    === PERFIL DO EXPLORADOR ===
    Nome: {perfil['nome']}
    Idade: {perfil['idade']} anos
    Nível Atual: {perfil['titulo']} (XP: {perfil['xp_atual']})
    
    === META (SONHO) ===
    Objetivo: {perfil['meta_atual']['nome']}
    Custo Total: R$ {meta_valor:.2f}
    Já Guardou: R$ {total_guardado:.2f}
    Falta: R$ {falta:.2f}
    
    === HISTÓRICO DO COFRINHO (Últimas transações) ===
    {cofrinho.tail(5).to_string(index=False) if not cofrinho.empty else "Nenhuma transação ainda."}
    
    === MISSÕES DISPONÍVEIS ===
    {json.dumps(missoes, indent=2, ensure_ascii=False)}
    
    === CONCEITOS QUE VOCÊ SABE ENSINAR (ENCICLOPÉDIA) ===
    {json.dumps(enciclopedia, indent=2, ensure_ascii=False)}
    """
    return contexto