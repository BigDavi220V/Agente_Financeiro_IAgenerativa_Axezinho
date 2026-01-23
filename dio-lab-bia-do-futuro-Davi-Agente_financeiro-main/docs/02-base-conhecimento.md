# Base de Conhecimento - Axézinho 🎒

## Dados Utilizados

A base de conhecimento do Axézinho foi simplificada para atender ao público infantil e à arquitetura de regras (sem IA generativa pesada).

| Arquivo | Formato | Para que serve no Axézinho? |
|---------|---------|---------------------|
| `perfil_explorador.json` | JSON | Define o "save" do jogador: nome, nível (XP), avatar, meta atual (ex: Skate) e conquistas desbloqueadas. |
| `enciclopedia_economia.json` | JSON | Funciona como o "cérebro" educativo. Contém conceitos (Escambo, 5 Rs) e explicações validadas pelo material didático. |
| `missoes.json` | JSON | Lista de desafios práticos (ex: "Reciclar lixo", "Guardar moeda") que geram engajamento e XP. |
| `cofrinho_virtual.csv` | CSV | Histórico visual de "Ganhos" (mesada) e "Trocas" (gastos), focado em ensinar para onde o dinheiro vai. |

---

## Adaptações nos Dados

Para tornar a experiência lúdica e segura, os dados originais do projeto "Edu" sofreram as seguintes transformações:

1.  **De Investidor para Explorador:** Substituímos o `perfil_investidor` (focado em risco/patrimônio) pelo `perfil_explorador`, focado em **Gamificação** (XP, Títulos e Metas visuais).
2.  **Conteúdo Curado:** O arquivo `produtos_financeiros.json` (CDB, LCI) foi removido. No lugar, criamos a `enciclopedia_economia.json` com base no PDF "Educação Financeira para Crianças", garantindo que o agente explique apenas conceitos adequados à idade (História do Dinheiro, Necessidade vs. Desejo).
3.  **Transações Simplificadas:** O CSV agora registra apenas categorias simples (Lanche, Brinquedo, Mesada) para facilitar a visualização em gráficos ou tabelas simples.

---

## Estratégia de Integração

### Como os dados são carregados?
Os dados são carregados diretamente pelo Python (`src/conteudo.py`) no início da execução do Streamlit, servindo como memória rápida para a lógica do jogo.

```python
import pandas as pd
import json

# Carregamento da memória do Axézinho
perfil = json.load(open('./data/perfil_explorador.json'))
enciclopedia = json.load(open('./data/enciclopedia_economia.json'))
missoes = json.load(open('./data/missoes.json'))
cofrinho = pd.read_csv('./data/cofrinho_virtual.csv')
```
Fluxo Padrão:
 1️⃣ "A criança faz uma pergunta"
 2️⃣ "O sistema identifica a intenção (dúvida, missão, progresso)"
 3️⃣ "Busca palavras-chave nos arquivos JSON"
 4️⃣ "Retorna a informação exata armazenada"
 >Exemplo:
 * Pergunta: “O que é escambo?”
 * Ação: Busca pelo conceito "Escambo" na enciclopédia
 * Resposta: Explicação fixa e validada, sem risco de erro ou alucinação
```

### Como os dados são usados no prompt?
> Diferente de um LLM que precisa de um "Contexto de Prompt", o Axézinho usa uma Lógica de Regras (Rule-Based). Ele busca palavras-chave na pergunta da criança e consulta os dados para montar a resposta.

```
 1️⃣ "A criança faz uma pergunta"
 2️⃣ "O sistema identifica a intenção (dúvida, missão, progresso)"
 3️⃣ "Busca palavras-chave nos arquivos JSON"
 4️⃣ "Retorna a informação exata armazenada"
 >Exemplo:
 * Pergunta: "O que é escambo?"
 * Ação: Busca pelo conceito "Escambo" na enciclopédia
 * Resposta: Explicação fixa e validada, sem risco de erro ou alucinação
```

# Exemplo de Estrutura de Dados
Abaixo, um exemplo de como as informações estão estruturadas para alimentar o jogo:

### 1. Perfil do Jogador (perfil_explorador.json)

### 1. Perfil do Jogador (perfil_explorador.json)
```json
{
  "nome": "Jack",
  "idade": 10,
  "titulo": "Explorador Iniciante",
  "xp_atual": 150,
  "meta_atual": {
    "nome": "Comprar Skate",
    "custo": 200.00,
    "guardado": 45.00
  }
}
```
### 2. Conteúdo Educativo (enciclopedia_economia.json)

```json
[
  {
    "conceito": "Desejo vs Necessidade",
    "explicacao": "Necessidade é o que a gente precisa pra viver (comida). Desejo é o que a gente quer ter (videogame).",
    "exemplo": "Água é necessidade. Refrigerante é desejo!"
  },
  {
    "conceito": "Os 5 Rs",
    "explicacao": "Poderes para salvar o planeta: Repensar, Recusar, Reduzir, Reutilizar e Reciclar.",
    "exemplo": "Usar o verso da folha para desenhar (Reutilizar)."
  }
]
```json