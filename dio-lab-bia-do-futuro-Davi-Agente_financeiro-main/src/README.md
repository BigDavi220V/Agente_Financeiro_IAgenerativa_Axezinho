# Passo a Passo de Execução

## Setup do Ollama

```bash
# 1. Instalar Ollama (ollama.com)
# 2. Baixar um modelo leve
ollama pull gpt-oss

# 3. Testar se funciona
ollama run gpt-oss "Olá!"
```

## Código Completo

Todo o código-fonte está no arquivo `app.py`.

## Como Rodar

```bash
# 1. Instalar dependências
pip install streamlit pandas requests

# 2. Garantir que Ollama está rodando
ollama serve

# 3. Rodar o app
streamlit run .\src\app.py
```

## Evidência de Execução

### Teste de Conhecimento

![image](../assets/Resposta%20sobre%20o%20conteudo%2001.png)

![image](../assets/Resposta%20sobre%20o%20conteudo%2002.png)

![image](../assets/Resposta%20sobre%20o%20conteudo%2003.png)

### Teste de Lógica e Comportamento (O Prompt Rígido)

![image](../assets/Teste%20de%20L%C3%B3gica%20e%20Comportamento%20%28O%20Prompt%20R%C3%ADgido%29%2001.png)

![image](../assets/Teste%20de%20L%C3%B3gica%20e%20Comportamento%20%28O%20Prompt%20R%C3%ADgido%29%2002.png)

![image](../assets/Teste%20de%20L%C3%B3gica%20e%20Comportamento%20%28O%20Prompt%20R%C3%ADgido%29%2003.png)

### 🧪 Teste de "Alucinação" (O que ele NÃO deve saber)

![image](../assets/Teste%20de%20Alucina%C3%A7%C3%A3o%20%28O%20que%20ele%20N%C3%83O%20deve%20saber%29.png)

É notório que aqui têm um pouco de alucinação, mas não muito grave, pois continua incetivando a guardar dinheiro pra atingir o objetivo do sonho.

### Responder perguntas em sequência

![image](../assets/Resposta%20em%20sequencia%20e%20zero%20alucinacao.png)

Aqui ele conseguiu responder todas as perguntas sem perder o raciocínio da sua missão em relação ao usuário. Também conseguiu responder tudo em uma única caixa de perguntas.

### 🛡️ Testes de Bloqueio de Investimentos (Anti-Risco)

![image](../assets/🛡️%20Testes%20de%20Bloqueio%20de%20Investimentos%20(Anti-Risco).png)

### 🛑 Testes de Ética e Comportamento

![image](../assets/Testes%20de%20Ética%20e%20Comportamento.png)