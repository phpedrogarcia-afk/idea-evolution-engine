# docs/intelligence/GOVERNED-CHANGE.md — Protocolo de Governança de Mudanças e Reversibilidade

> **NENHUMA MUTAÇÃO MATERIAL OCORRE SEM RASTREABILIDADE E AVALIAÇÃO DE RISCO.**
> *Inteligência propõe; Constituição e Autoridade decidem.*

---

## 1. O Fluxo de Mudança Governada

```text
[1. PROPOSE]    Elaborar a DecisionProposal com opções, tradeoffs e justificativa.
      ↓
[2. EVIDENCE]   Apresentar evidência ou baseline sustentando a necessidade da mudança.
      ↓
[3. REVIEW]     Submeter à verificação (conforme o nível de risco em ADVERSARIAL-REVIEW.md).
      ↓
[4. AUTHORIZE]  Verificar a matriz de autoridade (Humano para CRITICAL; Kernel para determinístico).
      ↓
[5. APPLY]      Aplicar a mutação atômica (all-or-nothing).
      ↓
[6. VERIFY]     Executar testes determinísticos e de regressão.
      ↓
[7. RECORD]     Registrar no DECISIONS-LEDGER.md e atualizar manifesto.
```

---

## 2. Reversibility Check (Checagem de Reversibilidade)
Antes de aplicar qualquer alteração estrutural ou técnica:
- A IA deve perguntar: **"Esta modificação pode ser revertida de forma limpa via Git ou reversão de versão sem corromper o estado histórico?"**
- Se a resposta for **NÃO**, o risco é automaticamente promovido para `CRITICAL` e exige autorização humana expressa.

---

## 3. Formato Canônico de DecisionProposal
Uma proposta de decisão não se confunde com a decisão final aprovada:

```markdown
### DecisionProposal: [Título da Proposta]
- **Problem:** Qual gap ou desafio arquitetural exige uma decisão?
- **Options Considered:** Lista de opções com análise de prós e contras.
- **Evidence:** Dados empíricos, benchmarks ou referências de doadores.
- **Tradeoffs:** O que ganhamos e o que perdemos com cada opção.
- **Recommended Option:** Opção recomendada e justificativa.
- **Reversibility:** Análise de impacto caso seja necessário reverter.
- **Test Plan:** Como a eficácia da decisão será verificada.
- **Revisit Conditions:** Condições explícitas sob as quais a decisão deve ser revisada.
```
