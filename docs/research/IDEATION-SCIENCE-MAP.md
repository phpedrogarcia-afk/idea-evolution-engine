# IDEATION-SCIENCE-MAP.md — Mapa Científico da Ideação e Epistemologia

> **Fundamentação Teórica da Maturação de Ideias em Sistemas Artificiais**

---

## 1. As Quatro Dimensões do Espaço de Ideação (Projeção C-K)

Inspirado na Teoria C-K (Concept-Knowledge Theory de Hatchuel & Weil), o espaço cognitivo de uma ideia é mapeado como uma projeção bidimensional:

```text
                     CONCEITO (C)              CONHECIMENTO (K)
               (Não-decidível / Desejado)    (Decidível / Verdadeiro/Falso)
             ┌─────────────────────────────┬─────────────────────────────┐
             │                             │                             │
PROBLEMA (P) │     Problem Concept         │      Problem Knowledge      │
             │   (A dor/visão formulada)   │  (Fatos empíricos da dor)   │
             │                             │                             │
             ├─────────────────────────────┼─────────────────────────────┤
             │                             │                             │
SOLUÇÃO (S)  │     Solution Concept        │     Solution Knowledge      │
             │   (O mecanismo proposto)    │ (Viabilidade técnica/custo) │
             │                             │                             │
             └─────────────────────────────┴─────────────────────────────┘
```

---

## 2. A Dinâmica da Investigação Epistêmica
1. **Expansão Conceitual ($C \to C$):** Criação de novas ramificações, analogias e contra-propostas (Regime de Discovery).
2. **Ativação de Conhecimento ($K \to C$):** Uso de evidências e fatos conhecidos para condicionar ou restringir conceitos.
3. **Validação e Teste ($C \to K$):** Formulação de hipóteses falsificáveis que geram novos fatos quando submetidas ao teste empírico (`READY_TO_TEST`).
4. **Acúmulo Estruturado ($K \to K$):** Dedução lógica e redução de contradições no `evidence_registry`.

---

## 3. Epistemologia Popperiana e Falsificacionismo Sequencial
O IEE adota a premissa de Karl Popper de que nenhuma quantidade de confirmações teóricas prova definitivamente uma ideia, mas uma única observação empírica incompatível pode refutar uma premissa crítica. Por isso, a investigação privilegia a **procura ativa por evidências desconformatórias** (`find_disconfirming_evidence`) sobre a validação adulatória.
