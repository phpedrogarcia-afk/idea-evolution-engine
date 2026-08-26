# Prompt: CRITIQUE 1 — LOGICAL & ASSUMPTIONS (v0.1)
id: `PROMPT-CRITIQUE-LOGICAL-v0.1`
stage: `CRITIQUE_1`
purpose: Foco exclusivo em coerência interna, premissas implícitas, falácias causais e contradições estruturais.

## Instructions
Analise a ideia com foco estrito em coerência lógica e fragilidade de premissas causais.

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
  "fragile_assumptions": ["string"],
  "contradictions": ["string"]
}
```
