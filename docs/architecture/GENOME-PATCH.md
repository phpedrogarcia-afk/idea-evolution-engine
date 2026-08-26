# GENOME-PATCH.md — Propostas de Mutação e Validação Determinística

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. Princípio Fundamental de Mutação
> **Inteligência propõe; Constituição decide.**

Nenhuma IA ou agente autônomo escreve diretamente sobre o `IdeaGenome`. Toda modificação no estado é empacotada como um **`GenomePatch`** e submetida ao **`GenomeValidator`** determinístico.

---

## 2. As 5 Camadas de Validação Determinística do Kernel

```text
┌─────────────────────────────────────────────────────────────┐
│                        GenomePatch                          │
│         (base_version, author, operations, basis)           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│ 1. SCHEMA VALIDATION                                        │
│    Validação formal de tipos e campos obrigatórios          │
├─────────────────────────────────────────────────────────────┤
│ 2. REFERENTIAL VALIDATION                                   │
│    Verifica integridade de IDs (claims, evidências, etc.)   │
├─────────────────────────────────────────────────────────────┤
│ 3. AUTHORITY VALIDATION                                     │
│    Verifica se o ator possui escopo de autoridade formal    │
│    (Proteção estrita a Protected Cores e decisões humanas)  │
├─────────────────────────────────────────────────────────────┤
│ 4. INVARIANT VALIDATION                                     │
│    Verifica conformidade com GOVERNANCE-INVARIANTS.md       │
├─────────────────────────────────────────────────────────────┤
│ 5. TRANSITION VALIDATION                                    │
│    Verifica se a transição é válida na Máquina de Estados   │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
       [TODAS PASSAM]                   [QUALQUER FALHA]
               │                               │
        Commit v(N+1)                   Rejeição Total
 (Grafo imutável atualizado)      (vN permanece byte-identical)
```

---

## 3. Atomicidade e Regras de Segurança
- **All-or-Nothing:** O patch é aplicado integralmente ou rejeitado por completo. Não existem mutações parciais.
- **Autoridade Confiável Externa:** A autoridade do ator não é inferida a partir de campos declarados dentro do payload JSON (`"actor": "human"`), mas sim a partir de um `ExecutionContext` fornecido pelo ambiente de execução seguro.
- **Detecção de Conflito de Versão:** Se `base_version` do patch for diferente da versão atual do genoma, o patch é sumariamente rejeitado para impedir condições de corrida.
