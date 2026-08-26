# AUTHORITY-MATRIX-v0.1.md — Matriz Formal de Autoridade

> **STATUS: SPECIFICATION CONGELADA — v0.1**

---

## 1. O Princípio da Soberania e Escopo de Autoridade
> **Capability != Authority.**

O `GenomeValidator` aplica uma matriz estrita de controle de acesso baseada em papéis e contextos de execução autenticados (`ExecutionContext`), impedindo que agentes de IA realizem mutações reservadas ao humano ou que extrapolem suas permissões contratuais.

---

## 2. Matriz de Permissões por Tipo de Operação

| Entidade / Operação no Genoma | Humano Criador (`HUMAN_OWNER`) | Kernel Determinístico (`KERNEL_CORE`) | Agente / Função de IA (`AI_AGENT`) |
| :--- | :---: | :---: | :---: |
| **Definição de Propósito Original (`purpose`)** | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado | ❌ Negado (Apenas Leitura) |
| **Criação / Modificação de `ProtectedCore`** | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado | ❌ Negado (Pode criticar / gerar report) |
| **Decisões Normativas / Valores (`HUMAN_DECISION_REQUIRED`)** | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado | ❌ Negado |
| **Autorização de Pivot Fundamental (`PIVOT_CANDIDATE`)** | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado | ❌ Negado (Pode propor branch) |
| **Arquivamento Definitivo (`ARCHIVED`)** | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado | ❌ Negado |
| **Validação e Commit de Versão ($v_N \to v_{N+1}$)** | ❌ Delegado ao Kernel | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado (Apenas propõe patch) |
| **Cálculo de Transição de Estados (State Machine)** | ❌ Delegado ao Kernel | ✅ **AUTORIDADE EXCLUSIVA** | ❌ Negado |
| **Proposta de Novas Claims e Relações** | ✅ Permitido | ❌ Reativo a Patch | ✅ **Permitido via GenomePatch** |
| **Registro de Evidências (`evidence_registry`)** | ✅ Permitido | ❌ Reativo a Patch | ✅ **Permitido com Proveniência** |
| **Registro de Tensões (`TensionRecord`)** | ✅ Permitido | ❌ Reativo a Patch | ✅ **Permitido via GenomePatch** |
| **Desenho de `TestContract`** | ✅ Permitido | ❌ Reativo a Patch | ✅ **Permitido via GenomePatch** |

---

## 3. Blindagem de Protected Cores e Core Pressure
- Quando um agente de IA identifica que uma evidência empírica ou crítica lógica colide com um `ProtectedCore`, o validador **REJEITA** qualquer tentativa de alteração direta do core.
- Em vez disso, o sistema gera um **`CorePressureReport`** marcando o status do núcleo como `UNDER_PRESSURE` ou `IN_CONFLICT`.
- O relatório é apresentado ao humano criador, que possui o direito soberano de:
  1. `HUMAN_REAFFIRMED`: Manter o core inalterado apesar da pressão.
  2. `HUMAN_AMENDED`: Modificar ou relaxar o core explicitamente.
  3. `BRANCH_PIVOT`: Criar uma nova branch exploratória mantendo o core original na linhagem principal.
