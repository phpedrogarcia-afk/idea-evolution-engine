# docs/intelligence/ADVERSARIAL-REVIEW.md — Protocolo de Revisão Adversarial e Verificação Baseada em Risco

> **PRODUCER != SOLE APPROVER.**
> *A IA que produz a solução não deve ser a única responsável por declarar sua correção em questões materiais.*

---

## 1. Modos de Revisão Formal

| Modo de Revisão | Descrição | Quando Aplicar |
| :--- | :--- | :--- |
| **`SELF_CHECK`** | Verificação autônoma do próprio autor contra checklists e linters. | Tarefas de baixo risco (LOW). |
| **`INDEPENDENT_REVIEW`** | Avaliação executada por um papel cognitivo desacoplado da criação. | Tarefas estruturais médias (MEDIUM). |
| **`ADVERSARIAL_REVIEW`** | Crítica intencional focada em encontrar falhas, contraexemplos e brechas. | Mudanças arquiteturais e de specs (HIGH). |
| **`DETERMINISTIC_VALIDATION`** | Validação mecânica executada por scripts (schemas, testes, hashes). | Obrigatório em todas as tarefas (100% dos commits). |
| **`HUMAN_REVIEW`** | Consulta soberana ao criador humano para aprovação normativa. | Mudanças constitucionais, pivots e protected cores (CRITICAL). |

---

## 2. Níveis de Risco e Intensidade de Verificação

```text
┌──────────────┬───────────────────────────────┬────────────────────────────────────────┐
│ Nível Risco  │ Exemplos de Mudança           │ Intensidade de Verificação Obrigatória │
├──────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ LOW          │ Correção de typos, markdown,  │ SELF_CHECK + DETERMINISTIC_VALIDATION  │
│              │ formatação semântica.         │                                        │
├──────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ MEDIUM       │ Adição de testes, novas       │ SELF_CHECK + INDEPENDENT_REVIEW +      │
│              │ fixtures, scripts auxiliares. │ DETERMINISTIC_VALIDATION               │
├──────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ HIGH         │ Novas políticas, alteração de │ ADVERSARIAL_REVIEW + TESTES DE         │
│              │ arquitetura, novos doadores.  │ MUTÇÃO + DETERMINISTIC_VALIDATION      │
├──────────────┼───────────────────────────────┼────────────────────────────────────────┤
│ CRITICAL     │ Invariantes, Protected Cores, │ DETERMINISTIC_VALIDATION + ADVERSARIAL │
│              │ transição de fase, soberania. │ + HUMAN_AUTHORITY_APPROVAL             │
└──────────────┴───────────────────────────────┴────────────────────────────────────────┘
```
