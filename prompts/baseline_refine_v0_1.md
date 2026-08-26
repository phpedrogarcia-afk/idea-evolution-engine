# Prompt: BASELINE REFINE (v0.1)
id: `PROMPT-BASELINE-REFINE-v0.1`
purpose: Prompt único genérico de refinamento representando a prática comum de um único modelo.

## Instructions
Por favor, analise cuidadosamente a seguinte ideia humana crua e proponha uma versão significativamente refinada, identificando problemas, alternativas e próximos passos recomendados.

## Input Context
- Idea: {idea}

## Output Schema (JSON estrito)
```json
{
  "summary": "string",
  "strengths": ["string"],
  "weaknesses": ["string"],
  "refined_version": "string",
  "next_steps": ["string"]
}
```
