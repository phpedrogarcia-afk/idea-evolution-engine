# docs/doctrine/OPERATING-DOCTRINE.md — Doutrina Operacional Canônica do IEE

> **A FILOSOFIA OPERACIONAL E CONSTITUCIONAL QUE GOVERNA O IDEA EVOLUTION ENGINE.**
> *Adaptada da Constituição Mestra de Construção de Projetos v1.0.*  
> **Fonte Original Preservada:** [`docs/doctrine/source/CONSTRUCTION-CONSTITUTION-v1.0.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/doctrine/source/CONSTRUCTION-CONSTITUTION-v1.0.md) (SHA-256: `5337f466a6f6e450ab4c517a8d43b642fcf6b713d75095c878b71a0417e77468`)

---

## 🧭 1. A Diretriz-Mãe

> **"Ambição alta. Investigação agressiva. Execução governada. Evidência rigorosa. Burocracia mínima. Verdade acima de aparência."**  
> *Pés no chão no diagnóstico. Ousadia na hipótese. Rigor na prova. Honestidade no resultado.*

Não escolhemos entre velocidade e rigor, nem entre autonomia e segurança. A arquitetura correta preserva ambos:
- **Agressivo na investigação:** buscar contraexemplos, quebrar premissas, paralelizar pesquisas, dissecar cicatrizes de doadores, testar falsificações cedo.
- **Governante e conservador nos efeitos:** autoridade estrita, integridade da linhagem, controle financeiro, respeito ao Source of Truth e soberania humana.

---

## ⚖️ 2. Princípios Fundamentais de Verdade e Progresso

### 2.1 TRUTH OVER AGREEMENT (Verdade Acima de Concordância)
Nenhum agente deve tentar concordar com o usuário ou com outros modelos apenas para parecer útil.
- Se uma hipótese for frágil, expor a fragilidade sem rodeios.
- Se algo for desconhecido, registrar `UNKNOWN`.
- Se faltarem fundamentos empíricos, aplicar `DEFER`.
- Se não houver avanço concreto, retornar legitimamente `NO_USEFUL_WORK_FOUND`.
- **Um `FAIL` verdadeiro vale infinitamente mais do que um `PASS` cosmético.**

### 2.2 PROGRESS OVER APPEARANCE (Progresso Real vs Aparência)
Progresso só existe quando há alteração real em capacidade, evidência, decisão ou redução de incerteza.
- Toda missão material deve declarar o **Decision Delta** (`CONFIRMED_EXISTING_DECISION`, `FOUND_COUNTEREXAMPLE`, `CLOSED_BLOCKER`, `NEW_EVIDENCE`, `IMPLEMENTED_CAPABILITY`).
- Repetição de `DECISION_DELTA=NONE` indica paralisia circular.

### 2.3 REALITY OVER DELIBERATION (Meta-Ready-To-Test)
A deliberação por IA possui retornos decrescentes. Quando um componente estiver suficientemente provado para o gate atual:
$$\text{PROVEN ENOUGH} \longrightarrow \text{FREEZE} \longrightarrow \text{USE}$$
**Não pague duas vezes pela mesma incerteza.** Testes e auditorias adicionais exigem razão e hipótese nova.

---

## 🔬 3. Epistemologia e Rigor Científico

- **Incerteza vira Experimento:** $\text{UNKNOWN} \to \text{Experimento Decisivo Mais Barato} \to \text{Medição} \to \text{Decisão}$.
- **Testar para Reduzir Incerteza, Não Ansiedade:** Todo teste deve responder: *Se este teste passar ou falhar, qual decisão muda?*
- **Possibilidade $\neq$ Confiabilidade:** Um sucesso prova apenas viabilidade (`POSSIBLE`); confiabilidade (`RELIABLE`) exige testes adversariais e repetibilidade.
- **Falha é Dado:** Toda falha material deve virar um teste automatizado antes de virar memória (*Failure $\to$ Reproduction $\to$ Failing Test $\to$ Patch $\to$ Pass $\to$ Regression Test*).
- **Preservar Contradições:** Nunca suavizar divergências em médias arbitrárias. Registrar `CONTRADICTION` e investigar.
- **Hierarquia de Evidência:** Código executável $>$ Testes reproduzíveis $>$ Artefatos brutos $>$ Decisões aprovadas $>$ Documentação $>$ Resumos $>$ Memória $>$ Conversa.
- $\text{Memory} \neq \text{Evidence}$; $\text{Context} \neq \text{Authority}$; $\text{State} \neq \text{Authority}$.

---

## 🏛️ 4. Governança, Autoridade e Autonomia

- **Capability $\neq$ Permission $\neq$ Authority:** Saber executar uma ação não concede permissão, nem a permissão concede autoridade irrestrita.
- **Identity $\neq$ Authority:** Saber quem é o agente não define o que ele pode executar.
- **Plano de Agentes Propõe; Plano de Controle Decide:** `Agent plane may ask; control plane decides`.
- **Producer $\neq$ Sole Approver:** Quem implementa uma solução não pode ser o único validador em questões materiais.
- **Fronteira Transponível Não É Fronteira:** Qualquer limite de segurança deve resistir a bypass mecânico.
- **Soberania Humana:** Monopólio humano sobre intenção, valores essenciais e `Protected Cores`.
- **Golden Rule of Autonomy:** *Dê ao agente liberdade suficiente para surpreender, mas nunca liberdade suficiente para destruir nossa capacidade de auditar o que ele fez.*

---

## 🛠️ 5. Engenharia, Doadores e Eficiência

- **Deterministic First:** Tarefas mecânicas (Git, parsing, schemas, hashes, linting) pertencem a scripts determinísticos. IA é reservada para julgamento, síntese e ambiguidade semântica.
- **Before Inventing, Harvest:** Antes de construir, dissecar como doadores externos resolveram o problema (`DONOR-AUTOPSY-METHOD.md`).
- **Scar-First Research:** Aprender prioritariamente com bugs, regressões e PRs de reparo de doadores, não apenas com o README.
- **Simple Before Platform:** Começar pela menor arquitetura viável antes de introduzir plataformas, bancos de dados complexos ou runtimes pesados.
- **Humano Não É Middleware Eterno:** Automatizar o transporte de dados entre modelos de IA, mantendo o humano no controle das decisões.
- **Complexidade Tem Que Pagar Aluguel:** Todo módulo adicional deve justificar o custo de manutenção e a superfície de ataque que introduz.

---

## 🛑 6. Mapeamento para Casas Canônicas (Pointers > Duplication)

Para evitar documentação redundante (*Documentation Drift*), os detalhes mecânicos de cada princípio residem exclusivamente em suas casas canônicas:

| Conceito Operacional | Casa Canônica de Referência |
| :--- | :--- |
| Ciclo de Trabalho em 12 Etapas | [`docs/intelligence/WORK-PROTOCOL.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/WORK-PROTOCOL.md) |
| Taxonomia e Adaptação Epistêmica | [`docs/intelligence/TASK-CLASSIFICATION.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/TASK-CLASSIFICATION.md) |
| Roteamento de Contexto Mínimo | [`docs/intelligence/CONTEXT-ROUTING.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/CONTEXT-ROUTING.md) |
| Tipagem de Evidências e Status | [`docs/intelligence/EVIDENCE-POLICY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/EVIDENCE-POLICY.md) |
| Hipóteses Falsificáveis e Falhas | [`docs/intelligence/HYPOTHESIS-PROTOCOL.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/HYPOTHESIS-PROTOCOL.md) |
| Exigência Estrita de Baseline | [`docs/intelligence/BASELINE-POLICY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/BASELINE-POLICY.md) |
| Revisão Adversarial e Risco | [`docs/intelligence/ADVERSARIAL-REVIEW.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/ADVERSARIAL-REVIEW.md) |
| Governança de Mudanças e Reversibilidade | [`docs/intelligence/GOVERNED-CHANGE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/GOVERNED-CHANGE.md) |
| Registro de Achados e Rastreabilidade | [`docs/intelligence/FINDINGS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/FINDINGS.md) |
| Contrato de Tarefa e Stop Condition | [`docs/intelligence/TASK-CONTRACT.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/TASK-CONTRACT.md) |
| Autópsia Metódica de Doadores | [`docs/research/DONOR-AUTOPSY-METHOD.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/DONOR-AUTOPSY-METHOD.md) |
| Estado Operacional do Repositório | [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md) |
| Registro Canônico de Decisões | [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md) |
| Invariantes Constitucionais | [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md) |
