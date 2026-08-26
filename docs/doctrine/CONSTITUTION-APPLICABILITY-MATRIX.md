# docs/doctrine/CONSTITUTION-APPLICABILITY-MATRIX.md — Matriz de Aplicabilidade Constitucional

> **RECONCILIAÇÃO ESTRUTURADA DOS 150 PRINCÍPIOS DA CONSTITUIÇÃO MESTRA DE CONSTRUÇÃO (v1.0) COM O IDEA EVOLUTION ENGINE.**
> *Preserva a proveniência da doutrina adaptando sua aplicação operacional sem contaminação.*

---

## 1. Categorias de Classificação

- **`UNIVERSAL`:** Aplica-se universalmente a qualquer trabalho ou raciocínio no IEE.
- **`IEE_NOW`:** Governa estritamente o desenvolvimento ativo presente (Fase 0 e MVP).
- **`IEE_LATER`:** Relevante para fases posteriores (runtime de produção, deliberação avançada, RL).
- **`FIOOS_SPECIFIC`:** Específico da arquitetura de kernel/SO do FioOS; isolado para não poluir o IEE.
- **`CONDITIONAL`:** Aplica-se condicionalmente quando a superfície existir (ex: gastos reais, escala).
- **`ALREADY_INSTITUTIONALIZED`:** Já formalizado no repositório antes desta missão.
- **`CONFLICT_REQUIRES_RECONCILIATION`:** Tensão identificada e resolvida explicitamente.

---

## 2. Matriz de Reconciliação por Blocos Temáticos

| Seção / Bloco | Princípio Central | Classificação IEE | Status de Aplicação no IEE |
| :--- | :--- | :---: | :--- |
| **§1 Diretriz-Mãe** | Ambição alta, investigação agressiva, execução governada, prova rigorosa. | `UNIVERSAL` | **Adotado** como norte mestre em `OPERATING-DOCTRINE.md`. |
| **§2 Truth Over Agreement** | Discordância apoiada em evidência; `FAIL` verdadeiro $>$ `PASS` cosmético. | `UNIVERSAL` | **Já Institucionalizado** em `GOVERNANCE-INVARIANTS.md`. |
| **§3 Progress Over Appearance** | Progresso real exige `DecisionDelta`; proibição de avanços ilusórios. | `UNIVERSAL` | **Adotado** e incorporado ao `TASK-CONTRACT.md`. |
| **§4 Rigor vs Conservadorismo** | *Aggressive in investigation; governed in effects.* | `UNIVERSAL` | **Já Institucionalizado** na Missão Mestre 03. |
| **§5 UNKNOWN $\to$ Experiment** | Incerteza vira o experimento decisivo mais barato. | `IEE_NOW` | **Adotado** no ciclo do `WORK-PROTOCOL.md`. |
| **§6 Proven Enough $\to$ Freeze** | *Do not pay twice for the same uncertainty.* | `IEE_NOW` | **Adotado**; base do fechamento da Fundação e [ADR-012](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md#adr-012). |
| **§7 Reduzir Incerteza $\neq$ Ansiedade** | Teste só roda se puder alterar uma decisão real. | `IEE_NOW` | **Adotado** na política de testes e `TASK-CONTRACT.md`. |
| **§8 Possibilidade $\neq$ Confiabilidade** | Distinguir `POSSIBLE` de `RELIABLE` e `PRODUCTION_READY`. | `UNIVERSAL` | **Já Institucionalizado** em `EVIDENCE-POLICY.md`. |
| **§9 Falhas são Dados** | Falha vira teste de regressão antes de virar memória. | `IEE_NOW` | **Já Institucionalizado** em `HYPOTHESIS-PROTOCOL.md`. |
| **§10 Preservar Contradições** | Proibição de harmonização forçada; manter `CONTRADICTION`. | `UNIVERSAL` | **Já Institucionalizado** em `docs/context/CONTRADICTIONS.md`. |
| **§11 a §16 Hierarquia de Evidência** | $\text{Código} > \text{Testes} > \text{Decisões} > \text{Docs} > \text{Memória} > \text{Conversa}$. | `UNIVERSAL` | **Já Institucionalizado** em `EVIDENCE-POLICY.md` e `SOURCE-OF-TRUTH.md`. |
| **§17 Conversation is Cache** | Repositório é memória durável; conversa é cache volátil. | `UNIVERSAL` | **Já Institucionalizado** em `CONTINUITY-CAPSULE.md`. |
| **§18 a §20 Cold Start & Context** | *Don't cut brain; cut rediscovery.* Escalonamento guiado por evidência. | `IEE_NOW` | **Já Institucionalizado** em `AI-START-HERE.md` e `CONTEXT-ROUTING.md`. |
| **§21 Deterministic First** | Tarefas mecânicas pertencem a scripts; IA para semântica. | `IEE_NOW` | **Já Institucionalizado** em `TASK-CLASSIFICATION.md`. |
| **§22 a §25 Economia de Recursos** | *Start with cheapest competent model*; medir antes de otimizar. | `IEE_NOW` | **Já Institucionalizado** em `BASELINE-POLICY.md`. |
| **§26 a §29 Políticas e Governança** | Formalizar o formalizável; governar semântica sem burocracia. | `UNIVERSAL` | **Adotado** em `OPERATING-DOCTRINE.md`. |
| **§30 a §39 Autoridade e Controle** | $\text{Capability} \neq \text{Authority}$; $\text{Identity} \neq \text{Authority}$; soberania humana. | `UNIVERSAL` | **Já Institucionalizado** em `AUTHORITY-MATRIX-v0.1.md`. |
| **§33 Leases, Territory, Workloads** | Identidade de workload, leases temporais e território de execução. | `FIOOS_SPECIFIC` | **Isolado no FioOS.** Não importar estruturas de kernel para o IEE agora. |
| **§40 a §43 Revisão e Papéis** | *Producer $\neq$ Sole Approver*; Guardian adversarial; sem papéis permanentes. | `IEE_NOW` | **Já Institucionalizado** em `ADVERSARIAL-REVIEW.md`. |
| **§44 a §49 Doadores e Cicatrizes** | *Before inventing, harvest.* Scar-first research; extrair mecanismos. | `UNIVERSAL` | **Já Institucionalizado** em `DONOR-AUTOPSY-METHOD.md`. |
| **§50 a §52 Engenharia Incremental** | *Simple before platform*; menor delta incremental; CLI antes de server. | `IEE_NOW` | **Adotado** como diretriz estrita da Missão 04 (Simple Loop MVP). |
| **§53 a §57 Experimentos e Compute** | Fidelidade de fontes (hashes/SHA); paralelismo de aprendizado. | `CONDITIONAL` | **Adotado** condicionalmente para campanhas de larga escala. |
| **§58 Cost Authority** | Default `NO_CASH_SPEND=TRUE`; novos gastos exigem autorização humana. | `CONDITIONAL` | **Adotado** condicionalmente (IEE atual possui zero gasto pago direto). |
| **§59 a §65 Test Budget & Mutação** | 1 $\to$ 10 $\to$ 100; mutação e fuzzing orientados a decisão. | `CONDITIONAL` | **Adotado** condicionalmente na validação de invariantes críticas. |
| **§66 a §70 Contratos de Missão** | Toda missão exige `STOP_CONDITION`, objetivo e escopo fechado. | `IEE_NOW` | **Já Institucionalizado** em `TASK-CONTRACT.md`. |
| **§71 Mission Compiler** | Compilador automático de planos de missão a partir de specs. | `IEE_LATER` | **Adiado (DEFER).** Não construir compilador antes de ter fluxo estável. |
| **§72 a §77 Eficiência de Agentes** | Divulgação progressiva de tools; persistir estado, não compute ocioso. | `IEE_NOW` | **Já Institucionalizado** em `CONTEXT-ROUTING.md` e `CURRENT-STATE.md`. |
| **§78 a §85 Autonomia e Maturidade** | Autonomia conquistada por evidência; ciclo $\text{IDEA} \to \text{FROZEN}$. | `UNIVERSAL` | **Adotado** em `CONSTITUTIONAL-MATURITY-MAP.md`. |
| **§86 a §93 Casas Canônicas e Anti-Círculo** | Pointers $>$ duplication; *Anti-Circle Rule* baseada em incerteza. | `UNIVERSAL` | **Adotado** em `OPERATING-DOCTRINE.md` e `WORK-PROTOCOL.md`. |
| **§94 a §100 Anti-astronautics** | Mecânica para mecânica; humano não é middleware; complexidade paga aluguel. | `IEE_NOW` | **Adotado** como norte de implementação do Simple Loop MVP. |
| **§101 a §110 Segurança e Agressividade** | *Ambition high, effects bounded.* Falha fechada na autoridade, aberta na curiosidade. | `UNIVERSAL` | **Já Institucionalizado** em `GOVERNANCE-INVARIANTS.md`. |
| **§111 a §125 Reconstruibilidade** | Projeto reconstruível a frio; Definition of Done; mínima burocracia suficiente. | `UNIVERSAL` | **Já Institucionalizado** na Missão Mestre 02 e 03. |
| **§126 a §137 Alicerce e Anti-Padrões** | 6 documentos fundacionais; catálogo de 18 anti-padrões proibidos. | `UNIVERSAL` | **Já Institucionalizado** em todo o repositório. |
| **§138 a §150 Regras Finais** | *Reality over deliberation*; não diminuir ambição, melhorar prova. | `UNIVERSAL` | **Adotado** como síntese filosófica do IEE. |

---

## 3. Síntese de Reconciliação
- **Conceitos FioOS Específicos Isolados:** Leases de processo, workloads de TCB, isolamento de hypervisor e territories de SO.
- **Conceitos IEE Reforçados:** *Reality Over Deliberation*, *Simple Before Platform*, *Decision Delta* e eliminação do humano como middleware de copy/paste.
- **Conflitos Encontrados:** Zero contradições irreconciliáveis. A Constituição valida integralmente as escolhas arquiteturais das Fundações 01, 02 e 03.
