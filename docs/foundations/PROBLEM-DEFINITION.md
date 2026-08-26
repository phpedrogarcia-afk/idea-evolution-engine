# PROBLEM-DEFINITION.md — Definição do Problema Humano e Operacional

> **Por que o Idea Evolution Engine é necessário e qual problema ele resolve**

---

## 1. O Problema Humano na Ideação Moderna
Ideias inovadoras e complexas raramente nascem prontas. Elas emergem como intuições imprecisas, perguntas embrionárias ou analogias difusas. Quando um criador tenta amadurecer uma ideia hoje, ele enfrenta múltiplos obstáculos cognitivos:
1. **Premissas Invisíveis:** Incapacidade de enxergar suposições tácitas que, se falsas, invalidam toda a tese.
2. **Viés de Confirmação:** Dificuldade em gerar contra-hipóteses e críticas adversariais severas à própria ideia.
3. **Lacuna de Evidência:** Desconhecimento sobre o estado real da arte, literatura científica ou experimentos anteriores.
4. **Desarticulação Estrutural:** Dificuldade em separar o *problema real* da *solução imaginada*, misturando hipóteses empíricas com escolhas de valores.

---

## 2. A Limitação do Processo Manual com Múltiplas IAs
Atualmente, criadores utilizam um fluxo empírico informal:

```text
Humano tem uma ideia
        ↓
Conversa com IA A (ex: brainstorming)
        ↓
Copia o resultado para IA B (ex: crítica/crítica adversarial)
        ↓
IA B aponta falhas ou reformula
        ↓
Leva para IA C (ex: estimativa de viabilidade)
        ↓
Retorna com a síntese para IA A
        ↓
Ideia amadurece aos poucos
```

### Onde Esse Processo Manual Falha:
- **Carga Cognitiva Excessiva no Humano:** O humano precisa selecionar qual modelo chamar, que contexto passar, qual instrução dar e em que ordem orquestrar.
- **Perda e Degradação de Contexto:** A cada cópia e cola entre janelas de chat, nuances críticas e restrições fundamentais são esquecidas ou alucinadas.
- **Ausência de Critérios de Término:** A conversa torna-se infinita; não há como saber quando a deliberação esgotou sua utilidade teórica.
- **Falsa Sensação de Progresso:** Modelos tendem a gerar textos cada vez maiores e mais elegantes, sem que qualquer nova evidência ou teste concreto tenha sido produzido.
- **Deriva de Intenção (Goal Drift):** IAs frequentemente alteram silenciosamente a premissa central da ideia do criador para ajustá-la a padrões genéricos de mercado.

---

## 3. A Solução do Idea Evolution Engine
O IEE transforma esse ciclo artesanal em um **protocolo de investigação epistemológica governada**:
- Substitui a cópia manual de texto por um grafo de estado estruturado (`IdeaGenome`).
- Substitui conversas informais por contratos formais prévios (`DeliberationContract`).
- Substitui sínteses floreadas por métricas de progresso estrutural e decisional.
- Conduz a ideia até a formulação do próximo teste discriminativo no mundo real (`READY_TO_TEST`).
