# PILOT-PROTOCOL.md — M05.4 Treatment-Delivery Pilot 01 Protocol

> **STATUS:** FROZEN_CALIBRATION_PILOT
> **DATA:** 2026-08-29
> **EXPERIMENTO PRINCIPAL:** EXP-M05.4-PROSPECTIVE-RERUN-20260829 (Attempt-003 preservado e imutável)
> **PROVEDOR:** groq | **MODELO:** openai/gpt-oss-120b

---

## 1. Objetivo do Piloto
Verificar se os tratamentos completos das Condições A, B e C conseguem ser entregues ponta a ponta em execução sequencial real contra o provedor Groq sem falhas de orquestração ou colapso estruturado.

## 2. Ideias de Calibração (Não são holdouts do M05.4)
1. **CAL-01:** Lista de compras compartilhada com aprendizado preditivo familiar.
2. **CAL-02:** Ferramenta de registro e invalidação de premissas decisórias para equipes remotas.

## 3. Ordem de Execução Sequencial
1. CAL-01-CONDITION_A (Baseline Single Refine)
2. CAL-01-CONDITION_B (Simple Loop 6-Stage)
3. CAL-01-CONDITION_C (Lean Loop L1 FioED)
4. CAL-02-CONDITION_A (Baseline Single Refine)
5. CAL-02-CONDITION_B (Simple Loop 6-Stage)
6. CAL-02-CONDITION_C (Lean Loop L1 FioED)

## 4. Orçamento Máximo de Chamadas
- Condição A: 2 × 1 = 2
- Condição B: 2 × 10 = 20
- Condição C: 2 × 2 = 4
- **TOTAL MÁXIMO:** 26 chamadas semânticas.

## 5. Regras de Entrega de Tratamento
- **Condição A:** DELIVERED se BaselineRefineOutput for admitido com texto substantivo.
- **Condição B:** DELIVERED se atingir candidato evoluído após síntese; PARTIALLY_DELIVERED se terminar como REFINEMENT_INCOMPLETE com candidato utilizável; NOT_DELIVERED se falhar antes de produzir candidato.
- **Condição C:** DELIVERED se LeanFirstPassOutput for admitido e atingir estado terminal legítimo com material substantivo; NOT_DELIVERED se FIRST_PASS_FAILED.
