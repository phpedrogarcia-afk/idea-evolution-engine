# docs/intelligence/CHECKLISTS.md — Checklists Operacionais de Agentes

> **CHECKLISTS VERIFICÁVEIS DE INÍCIO E TÉRMINO DE MISSÃO.**
> *A execução rigorosa destas checklists garante continuidade e integridade.*

---

## 🟢 1. Agent Start Checklist (Início de Missão)

Toda IA que assume uma tarefa neste repositório deve verificar mental ou computacionalmente:

- [ ] **1. Validador de Contexto Íntegro:** Executou `python tools/context/validate_context.py` e obteve código de saída 0.
- [ ] **2. Estado Atual Identificado:** Leu `AI-START-HERE.md` e `docs/context/CURRENT-STATE.md`.
- [ ] **3. Último Checkpoint Localizado:** Inspecionou o último checkpoint em `docs/context/checkpoints/`.
- [ ] **4. Tarefa Ativa Identificada:** Consultou `docs/context/ACTIVE-QUEUE.md` e confirmou que a tarefa está na fila `NOW`.
- [ ] **5. Classificação de Tarefa Realizada:** Classificou a tarefa (Mecânica, Semântica, Empírica, Normativa, Mista) conforme `TASK-CLASSIFICATION.md`.
- [ ] **6. Perfil de Contexto Selecionado:** Escolheu o perfil adequado (`FAST`, `DEEP`, `RESEARCH`, `IMPLEMENTATION`) conforme `CONTEXT-ROUTING.md`.
- [ ] **7. Limites de Autoridade Compreendidos:** Verificou o que é permitido (`CAN`, `MAY`) e o que é proibido (`MUST_NOT`).
- [ ] **8. Baseline Mapeado:** Se a tarefa alega melhoria mensurável, identificou o baseline prévio conforme `BASELINE-POLICY.md`.

---

## 🏁 2. Agent End Checklist (Término de Missão)

Ao concluir a tarefa e antes de entregar a resposta:

- [ ] **1. Critérios de Aceitação Verificados:** O objetivo foi cumprido conforme o `TaskContract`?
- [ ] **2. Testes e Evidências Executadas:** Todos os testes unitários e de validação passaram 100%?
- [ ] **3. Registro de Falhas e Limitações:** Falhas, becos sem saída ou `NO_USEFUL_WORK_FOUND` foram registrados honestamente?
- [ ] **4. Decisões e Achados Persistidos:** Novas decisões foram registradas em `DECISIONS-LEDGER.md` e achados em `FINDINGS.md`?
- [ ] **5. Estado Operacional Atualizado:** `docs/context/CURRENT-STATE.md` e `docs/context/ACTIVE-QUEUE.md` foram atualizados?
- [ ] **6. Checkpoint Emitido:** Um novo checkpoint imutável foi gerado em `docs/context/checkpoints/`?
- [ ] **7. Manifesto Sincronizado:** `context-manifest.json` e `intelligence-manifest.json` foram atualizados com novos hashes?
- [ ] **8. Validador Final Verde:** Executou `python tools/context/validate_context.py` e `python tools/intelligence/validate_intelligence.py` retornando código 0.
