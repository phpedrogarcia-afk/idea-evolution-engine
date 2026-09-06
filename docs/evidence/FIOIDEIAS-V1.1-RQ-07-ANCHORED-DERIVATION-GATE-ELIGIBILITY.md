# FIOIDEIAS V1.1 — RQ-07 Anchored Derivation Gate Eligibility

## Status

`RQ_07 = PASS`

`KNOWN_REGRESSION_SET = YES`

`BLIND_HOLDOUT = NO`

Base da missão: `6ce585e9a9121def957caebb8150144c76d096be` em
`fioideias/v1.1-decision-relevance`.

## ROOT_CAUSE

O `UNANCHORED_DERIVATION_GATE_LEAK` era uma cadeia, não um único `if`:

1. `LEAN_FIRST_PASS` permitia que o modelo produzisse vulnerabilidades, severidade,
   escolha normativa e próximo passo sem uma prova compacta de autoridade para cada
   afirmação material.
2. `EarlyEpistemicGate.evaluate()` consumia diretamente esses campos e podia promover
   a classificação do modelo para `MATERIAL_VULNERABILITY`,
   `BIFURCAÇÃO_NORMATIVA`, incerteza de realidade ou competição material.
3. A arbitragem de `NEXT_ACTION` confiava na ação produzida pelo modelo e em critérios
   de falseamento que podiam conter implementação prematura.
4. O mapper aplicava procedência tarde demais. Além disso, rotulava a interpretação
   de intenção como `VALID_USER_DERIVATION` sem prova e fazia a análise focada herdar
   a autoridade da vulnerabilidade que havia acionado o gate.
5. Não existia uma verificação explícita para rejeitar uma derivação que contradissesse
   o input, como “dependência exclusiva em auto-observação” quando A Testemunha declara
   múltiplas fontes externas e auto-observação.

## CODE_PATH

`provider output -> LeanFirstPassOutput -> EarlyEpistemicGate.evaluate -> focused escalation -> NextActionArbitrationPolicy -> EvolutionArtifactMapper -> HumanResultRenderer`

Superfícies corrigidas:

- `src/idea_evolution/domain/grounding.py`
- `src/idea_evolution/domain/early_epistemic_gate.py`
- `src/idea_evolution/domain/decision_relevance.py`
- `src/idea_evolution/orchestration/lean_loop.py`
- `src/idea_evolution/artifacts/evolution_artifact.py`
- `src/idea_evolution/artifacts/mapper.py`
- `src/idea_evolution/artifacts/provenance.py`
- `src/idea_evolution/rendering/human_result.py`

## FIX

- Introduzida procedência material compacta e explícita por `GateAuthority`:
  `basis`, `support_ref` e `derivation`.
- `USER_EXPLICIT` só é elegível quando a proposição é sustentada pelo input.
- `VALID_USER_DERIVATION` exige referência rastreável existente no input e derivação
  necessária; plausibilidade ou utilidade não bastam.
- `MODEL_HYPOTHESIS` continua disponível como possibilidade, mas recebe
  `gate_eligible = false`, severidade efetiva `UNCONFIRMED` e status
  `EVIDENCE_NEEDED` quando aplicável.
- Claims contraditórios ao input falham antes de qualquer promoção de autoridade.
- Gates material, normativo, de mecanismos concorrentes e de incerteza de realidade
  só consideram claims elegíveis.
- Próximos passos não ancorados em `DISCOVERY`, `VALIDATION` ou `UNKNOWN` são
  rebaixados para o teste de menor custo capaz de reduzir a incerteza. Critérios de
  falseamento que já exigem implementação são ignorados quando há alternativa
  observacional mais barata.
- A leitura de intenção produzida pelo modelo permanece `MODEL_HYPOTHESIS`.
- Uma análise focada nova não herda a autoridade da vulnerabilidade-alvo: permanece
  `MODEL_HYPOTHESIS`, `UNCONFIRMED` e não elegível para gate.
- O prompt e o renderer expõem as classes de procedência sem ocultar conteúdo
  exploratório.

## NEW_INVARIANTS

- `MODEL_HYPOTHESIS_CAN_TRIGGER_GATE = NO`
- `UNANCHORED_SEVERITY_IS_EFFECTIVE = NO`
- `INPUT_CONTRADICTION_CAN_GAIN_DERIVED_AUTHORITY = NO`
- `MODEL_INTERPRETATION_IS_HUMAN_INTENT = NO`
- `FOCUSED_ANALYSIS_INHERITS_TARGET_AUTHORITY = NO`
- `UNANCHORED_IMPLEMENTATION_CAN_DETERMINE_NEXT_ACTION = NO`
- `MODEL_POSSIBILITIES_REMAIN_AVAILABLE = YES`
- `USER_EXPLICIT_CAN_TRIGGER_LEGITIMATE_GATE = YES`
- `TRACEABLE_VALID_USER_DERIVATION_CAN_TRIGGER_GATE = YES`

O hash canônico dos sete arquivos do núcleo Lean V1.1 após a mudança autorizada é
`3fa70e0ede15888ee5650fa08572508748eef1462de0a8bd01aa4a66a58b151f`.
Os schemas compactos permanecem dentro do limite do transporte: first pass `3088`
bytes e focused escalation `2743` bytes.

## TEST_COUNT

- Suíte completa: `522 passed, 2 warnings`.
- Baseline anterior: `508` testes.
- Novos testes RQ-07: `14 passed`.
- Os dois warnings são pré-existentes/ambientais: coleta da classe Pydantic
  `TestabilityBinding` e cache do pytest sem permissão de escrita.

Os testes RQ-07 cobrem gates normativo e material, contradição, autoridade explícita,
derivação rastreável, severidade versus relevância decisória, ação prematura,
possibilidades exploratórias, degradação fail-closed, inglês, intenção interpretada,
o counterexample “Executar o protótipo” e não-herança de autoridade pela análise focada.

Fixtures antigas que precisavam continuar acionando gates legítimos receberam âncoras
explícitas equivalentes; suas asserções comportamentais não foram enfraquecidas.
Asserções antigas que promoviam automaticamente `human_intent` foram endurecidas para
exigir o novo status não autoritativo.

## REGRESSION_RUN_IDS

Comparação histórica:

| Caso | Run anterior | Run RQ-07 | SHA-256 normalizado do input |
|---|---|---|---|
| A — A Testemunha | `RUN-20260905_151147` | `RUN-20260906_072248` | `8d71cd0c3ab12c42a41492444569ba0ea047012f897f56ec1ee234d5483dbae3` |
| B — O Observado | `RUN-20260905_151152` | `RUN-20260906_072927` | `8dbb2f8176cb363666fd53342021b23850b6573e594573a97fc025bc218d71f9` |
| C — O Buscador | `RUN-20260905_151156` | `RUN-20260906_072505` | `f6683810264f23590b567bf221ae1de05f79b78ac366e8c498f73cc654849231` |

`original_idea` é idêntica entre arquivo normalizado, `input.json` antigo,
`input.json` novo e artefato de cada caso. Os arquivos não foram alterados.

Houve também o run intermediário B `RUN-20260906_072307`, que revelou a forma inglesa
“Develop a prototype engine”. Ele foi superado pelo run autorizado
`RUN-20260906_072927`, que por sua vez revelou a variante portuguesa mais sutil em que
o próprio critério de falseamento começava por “Executar o protótipo”. Os dois
counterexamples foram preservados como testes determinísticos.

## Comparação dos casos

### A — A Testemunha

- Antes: duas chamadas e escalação material baseada na afirmação contraditória de
  “dependência exclusiva em auto-observação”.
- RQ-07: uma chamada, `RETURN_NOW`, nenhuma crítica de exclusividade; três críticas do
  modelo permanecem visíveis como `UNCONFIRMED`, enquanto “Fabricação de observações
  sem vestígio verificável”, expressa no input, continua elegível e com severidade.
- Próximo passo passou de construção de protótipo para injeção de eventos conhecidos e
  comparação observacional.
- Resultado: `PASS` para contradição, gate e relevância decisória.

### B — O Observado

- Antes: `HUMAN_DECISION_REQUIRED` acionado exclusivamente por escolha normativa do
  modelo.
- RQ-07: `RETURN_NOW`, nenhuma decisão humana fabricada, duas críticas do modelo
  preservadas como `UNCONFIRMED` e a patologia explicitamente descrita “Apego do
  Observado a uma proposta” mantida como crítica ancorada.
- O run externo final ainda registrou “Executar o protótipo...” como
  `EVIDENCE_NEEDED`. Esse counterexample foi corrigido depois do run: a política atual
  pula o critério de falseamento implementacional e seleciona o critério observacional
  seguinte (“Validar manualmente as premissas...”); o texto exato está coberto por
  teste determinístico.
- Resultado: `PASS` para gates e procedência; `PASS_DETERMINISTIC_POST_RUN` para
  `NEXT_ACTION`.

### C — O Buscador

- Antes: `HUMAN_DECISION_REQUIRED` acionado por conteúdo normativo do modelo.
- RQ-07: não há bifurcação normativa fabricada. As patologias explicitamente nomeadas
  no input continuam capazes de acionar gate material legítimo; “Doença da busca
  infinita” acionou escalação focal.
- O run externo expôs que o texto novo da análise focada herdava a âncora do alvo. O
  mapper atual elimina essa herança e mantém a análise adicional como
  `MODEL_HYPOTHESIS/UNCONFIRMED`; o alvo original permanece ancorado. O caso exato está
  coberto por teste determinístico.
- Resultado: `PASS` para disponibilidade de gate legítimo e ausência de bifurcação
  normativa; `PASS_DETERMINISTIC_POST_RUN` para procedência da análise focada.

## Riqueza conceitual

Não houve colapso para saída vazia ou puramente defensiva. Os três novos runs mantêm
ideia refinada, críticas, premissas, incertezas e, quando geradas, alternativas. A
mudança deliberada é epistemológica: conteúdo não ancorado continua visível, mas deixa
de receber severidade efetiva, autoridade de gate ou poder de determinar decisão.

## KNOWN_LIMITATIONS

- Estes casos são um conjunto de regressão conhecido: não são holdouts cegos e não
  constituem nova evidência científica independente.
- Um run por caso prova comportamento observado, não confiabilidade populacional.
- Os ajustes finais de intenção, ação B e análise focada C foram derivados dos próprios
  runs e validados deterministicamente, sem novo envio ao provider. Portanto os JSONs
  externos preservam os counterexamples históricos e não devem ser apresentados como
  artefatos regenerados pela última linha de código.
- A validação de derivação é conservadora e lexical/estrutural; claims sem prova
  suficiente degradam para hipótese em vez de serem aceitos por plausibilidade.
- Possibilidades do modelo continuam podendo ser semanticamente ruins; a propriedade
  provada é que elas não ganham autoridade material/normativa silenciosamente.

## VERDICT

`UNANCHORED_DERIVATION_GATE_LEAK = RESOLVED_WITHIN_TESTED_ENVELOPE`

`RELEASE_BLOCKER_RESOLVED = YES`
