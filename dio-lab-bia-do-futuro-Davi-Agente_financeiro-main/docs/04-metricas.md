# Avaliação e Métricas - Axézinho 🎒

Como o Axézinho opera com uma arquitetura baseada em regras (sem LLM generativo), nossa avaliação foca na precisão da detecção de intenção e na eficácia da gamificação.

## Como Avaliar o Agente

A avaliação é dividida em dois pilares:

- **Testes de Lógica (Funcional):** Verificar se as palavras-chave acionam as regras corretas (ex: "comprar" deve acionar "Verificador de Necessidade").
- **Testes de Experiência (Gamificação):** Verificar se a criança entende a dinâmica de ganhar XP e se sente motivada a continuar.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de Sucesso |
| --------- | -------------- | ------------------ |
| **Precisão de Intenção** | O sistema identificou a palavra-chave correta? | Usuário digita "gastar" e o sistema responde com o fluxo de "Saída de dinheiro". |
| **Segurança Pedagógica** | O bloqueio de temas adultos funcionou? | Usuário pergunta sobre "Bitcoin" e o sistema redireciona para "Poupança" sem dar dicas de investimento. |
| **Engajamento (XP)** | A gamificação está funcionando? | O usuário completa uma missão e o saldo de XP/Nível é atualizado visualmente na hora. |
| **Didática** | A explicação veio da Enciclopédia correta? | Ao perguntar "O que é Juros?", a resposta é exatamente a definição simplificada do arquivo JSON. |

---

## Exemplos de Cenários de Teste

Execute estes testes para validar a lógica do `app.py`:

### Teste 1: Fluxo de Consumo Consciente

- **Ação:** Digitar "Quero comprar um slime de 20 reais".
- **Comportamento Esperado:** O agente deve detectar a intenção de compra e devolver a pergunta: *"Isso é um desejo ou uma necessidade?"*.
- **Resultado:** [ ] Passou [ ] Falhou

### Teste 2: Consulta Educativa (Enciclopédia)

- **Ação:** Perguntar "O que são os 5 Rs?".
- **Comportamento Esperado:** O agente deve buscar o termo no `enciclopedia_economia.json` e exibir a explicação sobre Reciclar/Reutilizar.
- **Resultado:** [ ] Passou [ ] Falhou

### Teste 3: Bloqueio de Conteúdo (Edge Case)

- **Ação:** Perguntar "Qual a melhor ação da bolsa para ficar rico?".
- **Comportamento Esperado:** O agente **NÃO** deve recomendar ativos. Deve responder com a mensagem padrão de segurança (ex: "Isso é magia de adulto, vamos focar no seu cofrinho?").
- **Resultado:** [ ] Passou [ ] Falhou

### Teste 4: Gamificação e Meta

- **Ação:** Perguntar "Quanto falta para o meu skate?".
- **Comportamento Esperado:** O agente deve ler o `perfil_explorador.json`, calcular (Meta - Guardado) e responder o valor exato que falta.
- **Resultado:** [ ] Passou [ ] Falhou

---

## Formulário de Feedback (Playtest com Crianças)

Ao testar com o público-alvo (8-12 anos), use perguntas adaptadas:

| Critério | Pergunta para a Criança | Nota (1-5 ⭐) |
| --------- | ---------- | ---------- |
| **Diversão** | "Você gostou de conversar com o Axézinho?" | ___ |
| **Clareza** | "Você entendeu o que ele explicou sobre dinheiro?" | ___ |
| **Motivação** | "Você ficou com vontade de cumprir as missões para ganhar XP?" | ___ |
| **Visual** | "Você gostou dos emojis e da barra de nível?" | ___ |

**Comentário da Criança:**

> (Ex: "Achei engraçado ele me chamar de gafanhoto", "Queria poder trocar a cor do cofrinho")

---

## Resultados Esperados

Após a rodada de testes, esperamos validar:

- **Zero Alucinação:** Como as respostas são fixas (hardcoded/JSON), a taxa de respostas inventadas deve ser 0%.
- **Retenção:** A criança deve interagir por pelo menos 3 turnos (Pergunta -> Resposta -> Nova Ação).
- **Segurança:** Nenhum conselho financeiro real (CVM/B3) deve ser emitido.
