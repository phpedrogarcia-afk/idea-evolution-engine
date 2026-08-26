# Prompt: CRITIQUE 2 — FEASIBILITY & REAL WORLD (v0.1)
id: `PROMPT-CRITIQUE-FEASIBILITY-v0.1`
stage: `CRITIQUE_2`
purpose: Foco exclusivo em viabilidade técnica, atrito de adoção, incentivos econômicos e gargalos físicos no mundo real.

## Instructions
Analise a versão revisada da ideia focando exclusivamente na viabilidade prática, física, econômica e comportamental no mundo real.

## Output Schema (JSON estrito)
```json
{
  "critical_issues": [
    {
      "issue": "string",
      "why_it_matters": "string",
      "severity": "HIGH | MEDIUM | LOW",
      "affected_part": "string"
    }
  ],
  "failure_modes": ["string"],
  "missing_information": ["string"]
}
```
