# AGENTS.md — Regras de Conduta para Agentes e IAs

> Este documento define as regras operacionais estritas para qualquer modelo de linguagem (LLM) ou agente autônomo operando neste repositório.

---

## 1. Regra Fundamental de Operação
1. **Leia [`AI-START-HERE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AI-START-HERE.md)** antes de realizar qualquer modificação ou análise.
2. **Respeite a fase ativa:** Atualmente estamos na **FASE 0 — FUNDAÇÃO**. Não gere código de produto, servidores, rotas, bancos de dados ou interfaces visuais.
3. **Não confunda TARGET com CURRENT:** Se um documento descreve um módulo futuro do DCE ou do IdeaGenome, ele é um alvo arquitetural, não código existente.
4. **Propostas, não mutações diretas:** IAs propõem artefatos, schemas ou patches; a autoridade de aceitação e as invariantes constitucionais são verificadas por regras determinísticas e supervisão humana.

---

## 2. Disciplina Conceitual e Epistemológica
- **Sem Turismo Tecnológico:** Não introduza bibliotecas, frameworks multiagente (LangChain, AutoGen, CrewAI, etc.) ou padrões arquiteturais sem um *gap* receptor explícito aprovado no [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).
- **Sem Falsa Certeza:** Marque explicitamente o status das afirmações:
  - `CONFIRMED`: Sustentado por teste ou fonte comprovada.
  - `PLAUSIBLE`: Coerente, mas não verificado.
  - `BORROWED_MODEL`: Adaptado de doador externo.
  - `DESIGN_HYPOTHESIS`: Suposição de design nossa a ser testada.
  - `SPECULATION`: Possibilidade teórica aberta.
  - `REJECTED`: Avaliado e descartado.
- **Preserve Contradições e Tensões:** Nunca force consenso ou suavize desacordos fundamentais em um resumo arbitrário. Registre-os como `TensionRecord`.

---

## 3. Disciplina de Código e Documentação
- **Uma Única Casa Canônica:** Cada conceito possui um único documento de referência. Documentos secundários devem apontar links markdown para o documento principal, sem duplicar definições.
- **Progress Over Prose:** Não adicione texto prolixo sem valor estrutural. Documentos devem ser densos, precisos, estruturados e navegáveis.
- **Código apenas se estritamente fundacional:** Nesta fase, apenas schemas JSON/Pydantic, testes de invariantes e scripts determinísticos de validação estão autorizados quando especificados na [`docs/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/ACTIVE-QUEUE.md).

---

## 4. Fronteira com o FioOS
- O **Idea Evolution Engine** é um sistema independente focado em epistemologia, deliberação, maturação de ideias e redução de incerteza.
- O **FioOS** é um sistema operacional de inteligência focado em autoridade, sandboxing, budgets, leases de execução e auditoria de ferramentas.
- O IEE não deve duplicar o kernel do FioOS, nem o FioOS deve decidir sobre a verdade de claims ou valores humanos.
