# docs/intelligence/CONTEXT-ROUTING.md — Política de Roteamento e Escalonamento de Contexto

> **POLÍTICA PARA MAXIMIZAR EFICIÊNCIA DE TOKENS E PRECISÃO COGNITIVA.**
> *Economia de contexto por roteamento estruturado, não por amputação de conhecimento.*

---

## 1. Princípio do Contexto Mínimo Suficiente
> **Minimum sufficient context não significa o menor contexto possível; significa o menor conjunto de dados que ainda garante uma decisão 100% correta e em conformidade com as invariantes.**

---

## 2. Matriz de Seleção de Perfis

| Perfil de Contexto | Custo Estimado | Quando Usar | Arquivos Iniciais Obrigatórios |
| :--- | :---: | :--- | :--- |
| **🟢 FAST ENTRY** | ~2k tokens | Inspeção de estado, status de bugs, tarefas mecânicas, consultas de fila ativa. | - `AI-START-HERE.md`<br>- `docs/context/CURRENT-STATE.md`<br>- `docs/context/ACTIVE-QUEUE.md` |
| **🟡 DEEP ENTRY** | ~8k tokens | Propostas de arquitetura, resolução de contradições, governança, políticas. | FAST ENTRY +<br>- `docs/GOVERNANCE-INVARIANTS.md`<br>- `docs/context/CONTINUITY-CAPSULE.md`<br>- `docs/TARGET-ARCHITECTURE.md`<br>- Specs relevantes (`docs/specs/`) |
| **🔵 RESEARCH ENTRY** | ~6k tokens | Investigação de lacunas teóricas, autópsias de doadores, epistemologia. | FAST ENTRY +<br>- `docs/research/DONOR-INDEX.md`<br>- `docs/research/DONOR-AUTOPSY-METHOD.md`<br>- `docs/context/RESEARCH-BACKLOG.md`<br>- Autópsia específica (`docs/research/donors/`) |
| **🟣 IMPLEMENTATION ENTRY** | ~10k tokens | Implementação autorizada de schemas, validators e suítes de teste. | FAST ENTRY +<br>- `docs/context/CONTINUITY-CAPSULE.md`<br>- `docs/intelligence/WORK-PROTOCOL.md`<br>- Specs e testes correspondentes |

---

## 3. Escalonamento Explícito de Contexto (Context Escalation)
Uma IA inicia sempre no perfil mais econômico adequado. Se durante a análise o agente constatar que faltam definições críticas ou regras de contorno, ele deve realizar o escalonamento explícito:

```text
[FAST ENTRY]
     │
     ▼
[Avaliação de Suficiência] ──► CONTEXT_SUFFICIENT ──► Executa a tarefa
     │
     ▼ (Falta detalhe de arquitetura ou regra?)
CONTEXT_INSUFFICIENT
     │
     ▼
[Escala para DEEP ENTRY / RESEARCH ENTRY]
     │
     ▼
CONTEXT_EXPANDED ──► Registra justificativa ──► Executa a tarefa
```

> **REGRA:** O escalonamento é uma decisão técnica válida. Nunca execute uma modificação em arquivo constitucional ou de spec operando apenas sob FAST ENTRY.
