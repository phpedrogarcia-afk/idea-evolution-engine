# EXECUTION-SUMMARY.md — Sumário Operacional da Execução Real M05.4-P1

> **SUMÁRIO OPERACIONAL DA EXECUÇÃO EXPERIMENTAL PROSPECTIVA**
> **EXPERIMENT_ID:** `EXP-M05.4-PROSPECTIVE-20260827`
> **STATUS:** `REAL_EXECUTION_COMPLETE / HUMAN_BLIND_REVIEW_PENDING`
> **AVALIAÇÃO DE VENCEDOR SEMÂNTICO:** NÃO REALIZADA (Pendente de avaliação humana cega)

---

## 1. Métricas Operacionais Consolidadas

- **Total de Ideias Holdout:** 8 ideias (`IDEA-01` a `IDEA-08`)
- **Total de Condições:** 3 (`CONDITION_A`, `CONDITION_B`, `CONDITION_C`)
- **Total de Células Executadas:** 24 / 24 (100% de sucesso)
- **Provedor Utilizado:** Groq
- **Modelo Utilizado:** `openai/gpt-oss-120b` (sem fallback)
- **Total de Chamadas Reais de Modelo:** 28 chamadas
  - `CONDITION_A` (Baseline): 8 chamadas (exatamente 1 por ideia)
  - `CONDITION_B` (Simple Loop): 8 chamadas
  - `CONDITION_C` (Lean L1 / FioED): 12 chamadas (média de 1.5 por ideia, máx 2)
- **Falhas de Provedor / Rede:** 0 falhas

---

## 2. Integridade do Cegamento e Hash Commitments

| Item de Integridade | Status / Hash |
| :--- | :--- |
| **Integridade do Pré-registro** | `PASS` (Todos os 8 arquivos conferidos antes da execução) |
| **Vazamentos de Metadados no Pacote Cego** | `0 VAZAMENTOS DETECTADOS` (`leak_count = 0`) |
| **Hash do Pacote Cego (`BLIND-REVIEW-PACKET.md`)** | `5bce05da6df708e6202c2ae289313f453944986afe8a7451023ae2715551e595` |
| **Hash do Reveal Compromissado (`BLIND-REVEAL.sha256`)** | `970b03ad8eece795dea11653e744d1b4b3a2314f0e6db5bd883c307fa8ff97b4` |
| **Status da Revelação** | `REVEAL_SEALED` (Mapeamento não revelado ao avaliador humano) |

---

## 3. Próximo Passo Humano

O operador humano deve abrir o arquivo [`BLIND-REVIEW-PACKET.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/BLIND-REVIEW-PACKET.md), preencher suas notas e rankings no formulário [`M05.4-HUMAN-REVIEW-TEMPLATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/M05.4-HUMAN-REVIEW-TEMPLATE.md) e congelar sua avaliação antes da abertura de `BLIND-REVEAL.json`.
