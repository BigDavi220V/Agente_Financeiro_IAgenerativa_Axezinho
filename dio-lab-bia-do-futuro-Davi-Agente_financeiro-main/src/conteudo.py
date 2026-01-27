import json
import pandas as pd
import os

def carregar_dados():
    """
    Carrega toda a base de conhecimento, incluindo o CSV de Flashcards do usuário.
    """
    try:
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        perfil = json.load(open(os.path.join(base_path, 'perfil_explorador.json'), encoding='utf-8'))
        enciclopedia = json.load(open(os.path.join(base_path, 'enciclopedia_economia.json'), encoding='utf-8'))
        missoes = json.load(open(os.path.join(base_path, 'missoes.json'), encoding='utf-8'))
        
        # Carrega CSVs (Cofrinho e Flashcards)
        cofrinho_path = os.path.join(base_path, 'cofrinho_virtual.csv')
        flashcards_path = os.path.join(base_path, 'flashcards.csv')
        
        cofrinho = pd.read_csv(cofrinho_path) if os.path.exists(cofrinho_path) else pd.DataFrame()
        flashcards = pd.read_csv(flashcards_path) if os.path.exists(flashcards_path) else pd.DataFrame()
            
        return perfil, enciclopedia, missoes, cofrinho, flashcards
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None, None, None, None, None

def gerar_contexto_llm(perfil, enciclopedia, missoes, cofrinho, flashcards):
    """
    Transforma os dados em um Prompt rico para o Llama 3.2:1b
    """
    # Formata Flashcards (Assume que o CSV tem colunas, pega as 2 primeiras independente do nome)
    quiz_txt = ""
    if not flashcards.empty:
        colunas = flashcards.columns
        for index, row in flashcards.iterrows():
            # Pega a coluna 0 como Pergunta e a 1 como Resposta (genérico)
            p = row[colunas[0]]
            r = row[colunas[1]] if len(colunas) > 1 else "Sem resposta"
            quiz_txt += f"P: {p} | R: {r}\n"

    # Formata Missões
    missoes_txt = ""
    for m in missoes:
        status = "✅" if m['status'] == 'concluido' else "⬜"
        missoes_txt += f"- {status} {m['titulo']}: {m['descricao']}\n"

    contexto = f"""
    === PERFIL DO ALUNO ===
    Nome: {perfil['nome']}, {perfil['idade']} anos.
    Meta: {perfil['meta_atual']['nome']} (Falta R$ {perfil['meta_atual']['custo'] - perfil['meta_atual']['guardado']:.2f})
    
    === DICIONÁRIO ECONÔMICO (Use estas definições) ===
    {json.dumps(enciclopedia, indent=2, ensure_ascii=False)}
    
    === FLASHCARDS DE RESPOSTAS RÁPIDAS (Sua Memória) ===
    {quiz_txt}
    
    === MISSÕES RECOMENDADAS ===
    {missoes_txt}
    """
    return contexto