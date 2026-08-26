# AI-START-HERE — Ponto de Entrada Canônico para IAs e Agentes

> **LEITURA OBRIGATÓRIA ANTES DE QUALQUER OPERAÇÃO NESTE REPOSITÓRIO.**
> *Este arquivo é o roteador de entrada do Idea Evolution Engine (IEE). Ele orienta sua cognição para o contexto correto sem desperdício de tokens.*

---

## 1. O Que É o Idea Evolution Engine (IEE)
O **Idea Evolution Engine** é um sistema de investigação deliberativa governada que reduz, organiza e torna acionável a incerteza ao redor de uma intenção humana. O sistema descobre o que precisa ser verdade, falso, conhecido ou testado para justificar o próximo passo racional daquela ideia — **sem transferir às máquinas a soberania sobre ela**.

### 🚫 O Que o IEE Explicitamente NÃO É:
- NÃO é um chat livre entre bots sem contrato ou consenso forçado por votação.
- NÃO é um gerador automático de startups ou fábrica de pitches superficiais.
- NÃO é um substituto do criador humano (*Capability != Authority*).
- NÃO é um módulo interno do FioOS (mantêm fronteira rígida de papéis).
- NÃO é um sistema medido por tamanho de texto (*Progress over Prose*).

---

## 2. Onde Estamos: Estado Operacional & Roadmap

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. FASE 0 — FUNDAÇÃO & HARDENING DE CONTINUIDADE            │
│    [CONCLUÍDA] Toda base conceitual, regras e checkpoints   │
├─────────────────────────────────────────────────────────────┤
│ 2. PRÓXIMO ALVO DE PRODUTO: SIMPLE IDEA EVOLUTION LOOP      │
│    [MVP HEURÍSTICO] Understand → Attack → Alternatives →    │
│    Reality Check → Synthesize → Review (Pipeline Simples)   │
├─────────────────────────────────────────────────────────────┤
│ 3. ARQUITETURA ALVO: DCE GOVERNADO & IDEA GENOME COMPLETO   │
│    [TARGET] Não implementado ainda; desenho para Fases 2–4  │
├─────────────────────────────────────────────────────────────┤
│ 4. DCE ADAPTATIVO / BUSCA MCTS / RL / FioOS INTEGRATION    │
│    [FUTURE RESEARCH] Hipóteses exploratórias para Fases 5–6 │
└─────────────────────────────────────────────────────────────┘
```

> **REGRA DE OURO:** NENHUM código de produto ou servidor web está autorizado a ser gerado agora. Estamos sob ponto de bloqueio de governança.

---

## 3. Seleção de Perfil de Contexto (Context Routing)
Não carregue o repositório inteiro. Escolha o perfil exato para a sua missão:

| Perfil | Quando Usar | Documentos a Ler |
| :--- | :--- | :--- |
| **🟢 FAST ENTRY** (~2k tokens) | Inspeção rápida de status e tarefas | 1. [`AI-START-HERE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AI-START-HERE.md)<br>2. [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md)<br>3. [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md) |
| **🟡 DEEP ENTRY** (~8k tokens) | Governança, arquitetura e contratos | FAST ENTRY +<br>4. [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md)<br>5. [`docs/context/CONTINUITY-CAPSULE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTINUITY-CAPSULE.md)<br>6. [`docs/TARGET-ARCHITECTURE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/TARGET-ARCHITECTURE.md) |
| **🔵 RESEARCH ENTRY** (~6k tokens) | Pesquisa de doadores e epistemologia | FAST ENTRY +<br>4. [`docs/research/DONOR-INDEX.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/research/DONOR-INDEX.md)<br>5. [`docs/context/RESEARCH-BACKLOG.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/RESEARCH-BACKLOG.md) |
| **🟣 IMPLEMENTATION ENTRY** | Schemas e testes de validação | FAST ENTRY +<br>4. [`docs/context/CONTINUITY-CAPSULE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTINUITY-CAPSULE.md)<br>5. [`docs/specs/`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/specs/) |

---

## 4. Invariantes Constitucionais & Doutrina Operacional
> **Doutrina Operacional Canônica:** [`docs/doctrine/OPERATING-DOCTRINE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/doctrine/OPERATING-DOCTRINE.md) (v1.0)  
> **Protocolo de Trabalho em 12 Etapas:** [`docs/intelligence/WORK-PROTOCOL.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/WORK-PROTOCOL.md)

1. **Truth over agreement:** Melhorar a qualidade da decisão, nunca maximizar concordância artificial.
2. **Progress over appearance (Progress over prose / Decision Delta):** Progresso exige mudança real em evidência, decisão ou redução de incerteza.
3. **Capability != Authority:** O humano detém autoridade exclusiva sobre intenção, valores e *Protected Cores*.
4. **Memory != Evidence:** Histórico de chat ou suposição de LLM não é evidência; toda evidência requer proveniência.
5. **Deterministic First:** O kernel determinístico valida; a IA atua nas bordas semânticas como proponente via `GenomePatch`.
6. **Reality over Deliberation (Proven Enough $\to$ Freeze & Use):** Quando a incerteza for respondida, congele e use. Não pague duas vezes pela mesma incerteza.
7. **State must survive the model:** O estado do projeto reside no repositório imutável e em checkpoints, nunca na memória efêmera da IA.

---

## 5. Protocolo Obrigatório de Sessão
- **Ao Iniciar:** Execute `python tools/context/project_status.py` ou leia `docs/context/CURRENT-STATE.md`.
- **Ao Terminar:** Atualize `CURRENT-STATE.md`, emita um novo checkpoint e execute `python tools/context/validate_context.py`.
- **Em Caso de Conflito Canônico:** Pare imediatamente (*Fail-Closed*) e registre a divergência em [`docs/context/CONTRADICTIONS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTRADICTIONS.md).
