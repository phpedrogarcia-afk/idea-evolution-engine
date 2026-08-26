# docs/context/CONTEXT-PROTOCOL.md — Protocolos Operacionais de Contexto

> **PROTOCOLOS DE INÍCIO, TÉRMINO, INTERRUPÇÃO, RETOMADA E PERFIS DE CONTEXTO.**
> *A integridade e continuidade do projeto dependem da observância estrita destes protocolos por qualquer IA ou agente.*

---

## 1. Perfis de Entrada de Contexto (Context Routing)

Para evitar sobrecarga de contexto (*Context Cost*), uma IA deve carregar apenas o perfil estritamente necessário para sua tarefa imediata:

### 🟢 1. FAST ENTRY (~2k tokens)
*Para orientação rápida, verificação de status e perguntas sobre onde estamos.*
1. [`AI-START-HERE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AI-START-HERE.md)
2. [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md)
3. [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md)

### 🟡 2. DEEP ENTRY (~8k tokens)
*Para análise de arquitetura, propostas conceituais e governança.*
- Leitura do FAST ENTRY +
1. [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md)
2. [`docs/context/CONTINUITY-CAPSULE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTINUITY-CAPSULE.md)
3. [`docs/TARGET-ARCHITECTURE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/TARGET-ARCHITECTURE.md)
4. [`docs/specs/`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/) (especificações relevantes à tarefa).

### 🔵 3. RESEARCH ENTRY (~6k tokens)
*Para pesquisa de doadores, análise de papers e epistemologia.*
- Leitura do FAST ENTRY +
1. [`docs/research/DONOR-INDEX.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/DONOR-INDEX.md)
2. [`docs/research/DONOR-AUTOPSY-METHOD.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/DONOR-AUTOPSY-METHOD.md)
3. [`docs/context/RESEARCH-BACKLOG.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/RESEARCH-BACKLOG.md)
4. Autópsia do doador específico em estudo (`docs/research/donors/`).

### 🟣 4. IMPLEMENTATION ENTRY (~10k tokens)
*Para tarefas autorizadas de código, schemas e testes.*
- Leitura do FAST ENTRY +
1. [`docs/context/CONTINUITY-CAPSULE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTINUITY-CAPSULE.md)
2. Schemas e fixtures relevantes
3. Testes unitários/adversariais correspondentes.

---

## 2. Template de TaskContract (Para Missões de Agentes)

Toda tarefa delegada a um modelo deve obedecer a esta estrutura:

```markdown
# TASK-[ID]: [Título da Tarefa]
- **Objetivo:** Descrição precisa e inequívoca do resultado esperado.
- **Por Que Agora:** Vínculo com a ACTIVE-QUEUE.md e o roadmap ativo.
- **Escopo Autorizado:** Arquivos e módulos autorizados para modificação.
- **Entradas e Contexto Canônico:** Lista de arquivos de leitura obrigatória.
- **Entregáveis:** Lista de artefatos a serem produzidos ou modificados.
- **Critérios de Aceitação:** Testes e condições necessárias para considerar a tarefa concluída.
- **Ações Proibidas (DO-NOT-DO):** O que o agente está expressamente proibido de fazer.
- **Evidência Exigida:** Testes executados, logs ou hashes resultantes.
- **Requisito de Checkpoint:** Se exige emissão de novo checkpoint imutável ao terminar.
- **Condição de Parada:** Ponto exato onde o agente deve parar e aguardar revisão.
```

---

## 3. Protocolos de Sessão

### 🚪 3.1 Session Start Protocol (Início de Sessão)
Ao iniciar uma sessão no repositório, qualquer IA deve executar a seguinte sequência mental/operacional:
1. Ler [`AI-START-HERE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AI-START-HERE.md).
2. Validar o contexto executando `python tools/context/validate_context.py` (ou verificando `context-manifest.json`).
3. Ler [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md).
4. Inspecionar o último checkpoint em [`docs/context/checkpoints/`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/).
5. Inspecionar [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md).
6. Verificar o estado do Git (`git status`).
7. Confirmar correspondência entre documentação e filesystem antes de efetuar qualquer alteração.

### 🏁 3.2 Session End Protocol (Término de Sessão)
Ao concluir uma missão ou bloco de trabalho relevante:
1. Atualizar [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md).
2. Atualizar [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md).
3. Registrar a entrega no [`docs/context/IMPLEMENTATION-HISTORY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/IMPLEMENTATION-HISTORY.md).
4. Se houver nova decisão ou tensão, atualizar `DECISIONS-LEDGER.md` ou `CONTRADICTIONS.md`.
5. Emitir novo checkpoint imutável via `python tools/context/create_checkpoint.py` (ou criando manualmente `CP-YYYYMMDD-NNN`).
6. Atualizar `context-manifest.json` com os novos hashes.
7. Executar `python tools/context/validate_context.py` para garantir integridade.

### ⏸️ 3.3 Interrupt / Resume Protocol (Interrupção e Retomada)
Se uma IA desaparecer ou a sessão for interrompida no meio de uma tarefa:
1. A nova IA executa o *Session Start Protocol*.
2. Verifica o último checkpoint registrado (`LATEST_CHECKPOINT`).
3. Executa `git status` e `git diff` para identificar quais arquivos estavam em modificação parcial (`PARTIAL`).
4. Consulta `CURRENT-STATE.md` para identificar a `ACTIVE_TASK` e o `NEXT_EXACT_STEP`.
5. Retoma exatamente do ponto de interrupção, **sem refazer** os passos já confirmados em testes.

---

## 4. Política de Documentos Obsoletos (Stale-Doc Policy)
Um documento é classificado sob um dos seguintes estados de frescor:
- **`CURRENT`:** Atualizado, sincronizado com o manifesto e representativo da realidade física.
- **`STALE`:** Não atualizado após alterações relevantes no sistema; requer reconciliação imediata.
- **`SUPERSEDED`:** Substituído por uma nova versão ou política; contém ponteiro para o sucessor.
- **`ARCHIVED`:** Histórico preservado para rastreabilidade; não possui efeito operacional ativo.

> **REGRA:** Uma IA nunca deve inferir atualidade apenas pela data de modificação no sistema de arquivos; a autoridade vem do manifesto e das invariantes.
