# FIOED-FORMAL-MODEL.md — Modelo Matemático e de Estado da Dinâmica Epistêmica do FioIdeias

> **STATUS:** `WORKING_MODEL` | `FORMAL_SPECIFICATION` | `CALIBRATION_PENDING`
> **OBJETIVO:** Definir formalmente os símbolos, conjuntos, métricas determinísticas e a máquina de estados finitos que governam o kernel epistêmico.
> **REGRA DE RIGOR:** Métricas computáveis são fatos observáveis; limiares de corte ($N, k$) são políticas a serem calibradas empiricamente no receptor (`MEASUREMENT != THRESHOLD`).

---

## 1. Espaço de Estados e Definições de Conjuntos

Seja o espaço de estados evolutivos $\mathcal{X}$. O estado no passo temporal $t \in \mathbb{N}_0$ é a tupla:

$$X_t = \langle S, R_t, H_t, E_t, U_t, M_t, A_t, T_t, D_t, C_t \rangle$$

### 1.1 Conjuntos e Tipos
- **Fonte Imutável ($S$):** $S = \{ s_0, s_1, \dots, s_k \}$, onde cada $s_i \in \text{SourceAnchor}$ possui hash imutável $h(s_i) = \text{SHA256}(\text{bytes}(s_i))$. $S_0$ representa a entrada inicial e $S_j$ ($j > 0$) representa revisões ou decisões posteriores do usuário.
- **Representações ($R_t$):** $R_t = \{ r_1, \dots, r_m \}$, com $r_j = \langle \text{id}, \text{type}, \text{source\_refs}, \text{content}, \text{claim\_status} \rangle$.
- **Hipóteses Candidatas ($H_t$):** $H_t = \{ h_1, \dots, h_p \}$, com $h_l \in \text{ProposalRecord}$ e $\text{ontology\_state}(h_l) \in \{ \text{CANDIDATE}, \text{DEFERRED}, \text{REJECTED} \}$.
- **Evidências ($E_t$):** $E_t = \{ e_1, \dots, e_q \}$, onde $e_k$ é um identificador de evidência externa auditável (ex: `EXP-xxx`, `DOI:xxx`).
- **Incertezas ($U_t$):** $U_t = \{ u_1, \dots, u_n \}$, onde $u_i$ é uma premissa aberta ou dependência não validada.
- **Memória Institucional ($M_t$):** $M_t = \langle \mathcal{N}_t, \mathcal{D}_t \rangle$, com $\mathcal{N}_t$ conjunto de `NegativeKnowledgeRecord` e $\mathcal{D}_t$ repositório de cicatrizes de doadores.
- **Autoridade ($A_t$):** $A_t \in \{ \text{HUMAN\_SOVEREIGN}, \text{HUMAN\_DECISION}, \text{EXTERNAL\_EVIDENCE}, \text{MODEL\_HYPOTHESIS} \}$.
- **Tensões ($T_t$):** $T_t = \{ \tau_1, \dots, \tau_v \}$, onde $\tau_i = \langle \text{claim}_A, \text{claim}_B, \text{unresolved\_reason} \rangle$.
- **Fronteira de Decisão ($D_t$):** $D_t = \{ d_1, \dots, d_w \}$, conjunto de ações e escolhas concretas disponibilizadas ao decisor humano.
- **Contabilidade de Custo ($C_t$):** $C_t = \langle \text{calls} \in \mathbb{N}_0, \text{tokens} \in \mathbb{N}_0, \text{lookups} \in \mathbb{N}_0 \rangle$.

---

## 2. Métricas Determinísticas Computáveis

### 2.1 Profundidade de Intermediário ($\text{IntermediaryDepth}$)
Seja $\mathcal{G}_t = (V_t, \mathcal{E}_t)$ o grafo direcionado acíclico de proveniência, onde $V_t = S \cup R_t \cup H_t$ e $(u, v) \in \mathcal{E}_t$ indica que o nó $v$ foi gerado a partir do nó $u$.
Para qualquer claim $c \in V_t$:
$$\text{IntermediaryDepth}(c) = \min_{s \in S} \text{dist}_{\mathcal{G}_t}(s, c)$$

**Política de Reancoragem na Fonte (Source Refresh):**
$$\text{SourceRefreshRequired}(c) \iff \text{IsHighImpactDecision}(c) \land \text{IntermediaryDepth}(c) \ge k_{\text{threshold}}$$
- *Nota de Calibração:* O limiar $k_{\text{threshold}} = 2$ é adotado como `TEST_FIXTURE_THRESHOLD`, sujeito à calibração com dados de receptores na missão M05.3.

### 2.2 Persistência Sem Evidência ($P_e$) e Risco de Apego
Para cada hipótese $h \in H_t$, seja $\tau_{\text{evidence}}(h)$ o instante da última associação de evidência $e \in E$ ou autoridade humana $a \in A$ a $h$:
$$P_e(h, t) = t - \tau_{\text{evidence}}(h)$$

**Política de Detecção de Risco de Apego (Attachment Risk):**
$$\text{AttachmentRisk}(h, t) \iff P_e(h, t) \ge N_{\text{threshold}} \land \Delta D_t(h) = \emptyset$$
- *Nota de Calibração:* O limiar $N_{\text{threshold}} = 2$ é adotado como `TEST_FIXTURE_THRESHOLD`. O gatilho não exclui a hipótese; ele bloqueia a alocação automática de chamadas adicionais e força sua preservação como mero candidato.

### 2.3 Vetor de Risco de Desvio ($\mathbf{DriftRisk}$)
$$\mathbf{DriftRisk}(X_t) = \begin{bmatrix} 
| \{ c \in H_t \mid \text{grounding}(c) = \text{INVALID} \} | \\ 
\max_{c \in H_t} \text{IntermediaryDepth}(c) \\ 
\max_{h \in H_t} P_e(h, t) \\ 
\sum_{\tau \in T_t} 1 \\ 
\mathbb{I}(\text{AuthoritySpoofingDetected}) 
\end{bmatrix}$$

---

## 3. Máquina de Estados Finitos do FioED

```text
               ┌───────────────────────┐
               │    [01] UNINITIALIZED │
               └───────────┬───────────┘
                           │ Init(Input)
                           ▼
               ┌───────────────────────┐
               │   [02] SOURCE_ANCHORED│
               └───────────┬───────────┘
                           │ O(S) [Deterministic: Non-generative]
                           ▼
               ┌───────────────────────┐
               │      [03] OBSERVED    │
               └───────────┬───────────┘
                           │ I(O(S)) [Model Call 1]
                           ▼
               ┌───────────────────────┐
               │    [04] REPRESENTED   │
               └───────────┬───────────┘
                           │ A(X_t) [Attention: Snapshot A]
                           ▼
               ┌───────────────────────┐
               │      [05] ATTENDED    │
               └───────────┬───────────┘
                           │
             ┌─────────────┴──────────────────────────────┐
             │ Early Gate Evaluation Γ(F_t) [Cost = 0]    │
             ├────────────────────────────────────────────┤
             ├──▶ RETURN_NOW ─────────────▶ [06] COMPLETED_DIRECT (1 call)
             ├──▶ REQUEST_HUMAN ──────────▶ [07] HUMAN_DECISION_REQUIRED (1 call)
             ├──▶ STOP_NO_USEFUL_WORK ────▶ [08] TERMINATED_NO_WORK (1 call)
             └──▶ ESCALATE_FOCUSED        │
                                          ▼
                               ┌───────────────────────┐
                               │  [09] RENT_CHECKED    │
                               └──────────┬────────────┘
                                          │ C_h(X_t) [Model Call 2: Max Calls = 2]
                                          ▼
                               ┌───────────────────────┐
                               │   [10] CONCENTRATED   │
                               └──────────┬────────────┘
                                          │ A(X_{t+1}) [Re-Attention: Global Recheck]
                                          ▼
                               ┌───────────────────────┐
                               │   [11] RE_ATTENDED    │
                               └──────────┬────────────┘
                                          │
                        ┌─────────────────┴─────────────────┐
                        ├──▶ No Progress ─▶ [12] NO_PROGRESS_STOP (2 calls)
                        └──▶ Progress ────▶ [13] COMPLETED_ESCALATED (2 calls)
```

---

## 4. Tabela Canônica de Transições de Estado

| Estado Atual | Evento / Operação | Pré-condição | Próximo Estado | Custo em Chamadas |
| :--- | :--- | :--- | :--- | :---: |
| `UNINITIALIZED` | `AnchorInput(text)` | $text \neq \emptyset$ | `SOURCE_ANCHORED` | 0 |
| `SOURCE_ANCHORED` | `Observe()` | $S$ imutável | `OBSERVED` | 0 |
| `OBSERVED` | `LeanFirstPass()` | Provedor disponível | `REPRESENTED` | 1 |
| `REPRESENTED` | `TakeAttentionSnapshot()` | Schemas válidos | `ATTENDED` | 0 |
| `ATTENDED` | `EarlyGate: RETURN_NOW` | Sem incertezas severas | `COMPLETED_DIRECT` | 0 (Total 1) |
| `ATTENDED` | `EarlyGate: HUMAN_REQ` | Escolha normativa requerida | `HUMAN_DECISION_REQUIRED` | 0 (Total 1) |
| `ATTENDED` | `EarlyGate: ESCALATE` | Risco HIGH / Alternativas | `RENT_CHECKED` | 0 |
| `RENT_CHECKED` | `FocusedEscalation(h)` | $\text{calls} < 2 \land \text{Rent} \in \{ \text{JUSTIFIED}, \text{EXPLORATORY} \}$ | `CONCENTRATED` | 1 (Total 2) |
| `CONCENTRATED` | `ReAttend()` | Saída da chamada 2 parsed | `RE_ATTENDED` | 0 |
| `RE_ATTENDED` | `CheckProgress()` | $\Delta D_t \neq \emptyset$ | `COMPLETED_ESCALATED` | 0 (Total 2) |
| `RE_ATTENDED` | `CheckProgress()` | $\Delta D_t = \emptyset$ (Stall) | `NO_PROGRESS_STOP` | 0 (Total 2) |
