# READY-TO-TEST.md — O Veredito de Transição Empírica

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. Definição Canônica de READY_TO_TEST
> **`READY_TO_TEST` ocorre quando existe um teste no mundo real capaz de produzir informação decisória relevante e nenhuma investigação puramente deliberativa claramente superior permanece disponível a custo proporcional.**

### 🚫 O que READY_TO_TEST Explicitamente NÃO É:
- **NÃO é uma nota de qualidade da ideia** (não significa que a ideia é boa ou ruim).
- **NÃO é um selo de aprovação ou sucesso**.
- **NÃO é um consenso entre IAs**.
- **NÃO é a conclusão final definitiva da ideia**.

`READY_TO_TEST` é estritamente um **veredito sobre a fonte do próximo conhecimento**: declara que a deliberação teórica atingiu retornos decrescentes e que o avanço epistêmico exige contato com a realidade empírica.

---

## 2. O TestContract (Contrato de Teste Empírico)
Ao atingir `READY_TO_TEST`, o sistema formula um `TestContract` estruturado contendo:

```text
TestContract
├── contract_id: UUID
├── target_claim: ID da claim crítica a ser testada
├── rival_hypotheses: Hipóteses concorrentes que explicam o mesmo fenômeno
├── measurable_implications: Consequências observáveis e mensuráveis se a claim for verdadeira
├── test_method: Protocolo do teste empírico (ex: entrevista, benchmark, protótipo descartável, landing page)
├── possible_outcomes: Mapeamento discreto de resultados possíveis
├── decision_effect_per_outcome: O que muda no genoma para cada resultado observado
├── stopping_rule: Regra para interromper o teste empírico
├── evidence_protocol: Como os dados brutos do teste serão convertidos em EvidenceRegistry
├── budget_and_risks: Custo, tempo limite e riscos operacionais do teste
└── reopen_conditions: Critérios para revisar o teste se o contexto externo mudar
```

---

## 3. Retorno ao Ciclo Epistêmico
Após a execução do teste empírico no mundo real, os resultados entram no `IdeaGenome` como novas instâncias no `evidence_registry` (`EXPERIMENT_RESULT`), e a ideia transiciona de volta para `DECISIONAL_INVESTIGATION` para absorver os aprendizados.
