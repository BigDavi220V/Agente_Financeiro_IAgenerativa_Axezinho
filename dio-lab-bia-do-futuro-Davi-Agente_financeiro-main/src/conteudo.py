import json
import pandas as pd
import os

def carregar_dados():
    """
    Carrega os arquivos JSON e CSV da pasta data/.
    Retorna None se algum arquivo estiver faltando.
    """
    try:
        base_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        
        perfil = json.load(open(os.path.join(base_path, 'perfil_explorador.json'), encoding='utf-8'))
        enciclopedia = json.load(open(os.path.join(base_path, 'enciclopedia_economia.json'), encoding='utf-8'))
        missoes = json.load(open(os.path.join(base_path, 'missoes.json'), encoding='utf-8'))
        
        csv_path = os.path.join(base_path, 'cofrinho_virtual.csv')
        if os.path.exists(csv_path):
            cofrinho = pd.read_csv(csv_path)
        else:
            # Cria um dataframe vazio se não existir
            cofrinho = pd.DataFrame(columns=['data', 'descricao', 'tipo', 'valor', 'categoria'])
            
        return perfil, enciclopedia, missoes, cofrinho
    except FileNotFoundError as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None, None, None, None

def buscar_conceito(termo, enciclopedia):
    """
    Procura um termo na enciclopédia (busca simples por palavra-chave).
    """
    termo = termo.lower()
    for item in enciclopedia:
        if item['conceito'].lower() in termo or termo in item['conceito'].lower():
            return f"🤓 **{item['conceito']}:** {item['explicacao']}\n\n*Exemplo:* {item['exemplo']}"
    return None