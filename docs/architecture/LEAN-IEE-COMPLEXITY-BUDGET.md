# LEAN-IEE-COMPLEXITY-BUDGET.md — Orçamento de Complexidade do Lean IEE

> **STATUS: TARGET / DESIGN_HYPOTHESIS**
> **OBJETIVO:** Justificar rigorosamente cada componente proposto no Lean IEE contra evidências empíricas e de doadores, aplicando o *Simplicity Challenge*. Componentes sem justificativa estrita são descartados ou adiados.

> **STATUS:** `DESIGN_BUDGET_VERIFIED`

---

## 1. Tabela de Justificação de Componentes

| Componente | Problema Resolvido | Evidência / Doador | Custo de Chamadas | Complexidade de Estado | Risco de Autoridade | Modo de Falha | Por que não mais simples? | Decisão |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- | :---: |
| **SourceAnchor** | Perda do texto e intenção original do usuário | FioIdeias Invariant / M05.1-R2 | 0 | Muito Baixa (string imutável) | Zero | Nenhum | Impossível ser mais simples | **`KEEP`** |
| **Lean First Pass Stage** | Obter intenção estruturada, mecanismo e premissas | Baseline A / Stanford Ideator | 1 | Baixa (JSON schema Pydantic) | Médio (hipótese do modelo) | Prolixidade ou premissas fracas | 1 chamada é o mínimo teórico para IA | **`KEEP`** |
| **Early Epistemic Gate** | Desperdício de inferência pré-gate (Epistemic Waste) | EXP-M05.2 / Magentic-One | 0 | Muito Baixa (regras determinísticas) | Zero (veto mecânico) | Falso positivo / Falso negativo na escalação | Se omitido, cai no desperdício de 10 chamadas | **`KEEP`** |
| **AuthorityProofValidator** | Spoofing de autoridade do usuário por IA | EXP-M05.1-R5 / FioOS | 0 | Muito Baixa (validador de string e proveniência) | Zero | Rebaixar premissa legítima para hipótese | Omitir permite usurpação de autoridade | **`KEEP`** |
| **Conditional Critique Stage** | Vulnerabilidade grave ou premissa frágil não testada | MultiAgent Ideator / DCI | 1 (sob gatilho) | Baixa (lista de críticas e mitigação) | Zero | Crítica superficial | Omitir deixa premissas frágeis sem contestação | **`ADAPT (CONDITIONAL)`** |
| **Conditional Alternatives Stage** | Múltiplos mecanismos concorrentes para a mesma intenção | Google Co-Scientist / Arbor | 1 (sob gatilho) | Baixa (2-3 alternativas com trade-offs) | Baixo | Adicionar opções óbvias | Omitir fecha opções técnicas cedo demais | **`ADAPT (CONDITIONAL)`** |
| **NegativeKnowledge Memory** | Repetição de mecanismos falhos em execuções anteriores | Arbor / IDEAgent | 0 | Baixa (lista de tuplas de falhas) | Zero | Bloquear reabertura válida | Omitir faz o sistema pagar 2x pela mesma falha | **`KEEP (OFFLINE)`** |
| **Fixed Multi-Stage Pipeline (6-10 calls)** | Esteira rígida para todas as ideias | EXP-M05.2 (Perdeu para baseline de 1 call) | 6 a 10 | Alta | Alto (acumula alucinações) | Aluguel de complexidade não pago | Provou ser ineficiente no M05.2 | **`REPLACE (CONTROL ONLY)`** |
| **Vector DB / RAG Semântico** | Recuperação semântica de doadores e memória | Anti-Turismo Tecnológico | 0 (mas pesada em runtime) | Alta (dependências externas) | Médio | Recuperar contexto irrelevante | Catálogo determinístico resolve no MVP | **`DEFER`** |
| **Multi-Agent Runtime Framework** | Orquestração de múltiplos agentes em paralelo | Stanford Ideator Scars | $N \times \text{calls}$ | Muito Alta | Alto | Falha de coordenação e custo explosivo | Piora a relação Decision Value / Call | **`REJECT`** |

---

## 2. Veredito do Orçamento
- O Lean IEE opera em **1 chamada nominal** (custo idêntico ao Baseline A) e **máximo 2 chamadas** quando ocorre escalação justificada por risco material.
- Redução de complexidade de chamadas de **$10 \to 1$ ou $2$** (economia de 80% a 90% em tokens comparado ao Simple Loop fixo).
- 100% dos componentes determinísticos de segurança e autoridade são mantidos a custo zero de inferência.
