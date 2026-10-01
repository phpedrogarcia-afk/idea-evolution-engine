# FioIdeias V1.1 — RQ-09 Epistemic Claim Boundary

MISSION_ID=FIOIDEIAS-V1.1-RQ-09-EPISTEMIC-CLAIM-BOUNDARY | DATE=2026-09-30
BRANCH=fioideias/v1.1-decision-relevance
START_HEAD=53d93b1175b9af57a60062d7aa03bcb2186e858d
RQ08_EVIDENCE_HEAD=53d93b1175b9af57a60062d7aa03bcb2186e858d
LAST_PRODUCT_CANDIDATE=d10ab406d048c44237d33e52b09f335fbaba4642
D10AB_ANCESTOR_OF_START_HEAD=YES

## Resultado

RQ08_BLOCKER_CONFIRMED=YES | FIX=EXPLICIT_EPISTEMIC_STATUS_FOR_MODEL_HYPOTHESIS_CANDIDATES
MODEL_HYPOTHESIS_CAN_SILENTLY_BECOME_FACT_IN_HUMAN_RENDERING=NO
CREATIVE_HYPOTHESES_PRESERVED=YES | RQ07_GATE_INVARIANTS_PRESERVED=YES
RQ08_BLOCKER_REPRODUCED_AFTER_FIX=NO | KNOWN_REGRESSION_SET=YES
BLIND_EVIDENCE=NO | NEW_GENERALIZATION_EVIDENCE=NO

The correction is limited to the human rendering boundary. Candidate text is
preserved verbatim, but each `MODEL_HYPOTHESIS` candidate now carries a visible
status stating that its mechanism, justification, and trade-offs are unverified
and must not be read as established facts. No model prompt, authority rule,
gate, schema, treatment, or product architecture changed.

## Estado inicial preservado

At mission start, `git status --short --branch` showed the required branch at
`53d93b1`, tracking the same origin branch, with no staged changes. The
worktree already contained 181 dirty paths: one modified tracked file
(`src/idea_evolution/cli/__pycache__/main.cpython-314.pyc`) and 180 untracked
files/directories, including user inputs and historical run artifacts. The
RQ-08 evidence commit existed and was the input HEAD; `d10ab406...` was its
ancestor. No cleanup, reset, checkout, or normalization was performed. The
pre-existing `.pyc` remains modified and is excluded from the RQ-09 commit; as
it was already dirty and was not snapshotted before Python invocations, this
record does not claim byte-for-byte preservation of its prior dirty contents.
Five untracked test-run directories appeared during the full-suite run; they
were retained and excluded from the RQ-09 commit.

`python tools/context/project_status.py` also reported a pre-existing context
integrity failure: manifest hash mismatches for `README.md`,
`docs/context/CURRENT-STATE.md`, and `docs/context/ACTIVE-QUEUE.md`, plus a
phase mismatch in `CURRENT-STATE.md`. These unrelated context inconsistencies
were left untouched under this mission's narrow scope.

## Autópsia exata do RQ-08

Fontes examinadas:

- `docs/evidence/FIOIDEIAS-V1.1-RQ-08-FINAL-BLIND-RELEASE-GATE.md`
- `docs/evidence/final-blind/CASE-A-EVALUATION.md`
- `docs/evidence/final-blind/CASE-B-EVALUATION.md`
- `docs/evidence/final-blind/CASE-C-EVALUATION.md`
- Preserved stdout and artifacts, now byte-preserved in the external archive recorded by [FIOIDEIAS-V1.1-RELEASE-TREE-HYGIENE-ARCHIVE.md](FIOIDEIAS-V1.1-RELEASE-TREE-HYGIENE-ARCHIVE.md)

### Claims que materializaram o bloqueio

| Caso | Claim / localização | Propósito e uso posterior | Suporte na fonte | Proveniência / status |
|---|---|---|---|---|
| B | `candidate_possibilities[0].justification`: “Solução de baixo esforço que evita riscos de estabilidade e segurança associados a ROMs customizadas.” | Justificar a alternativa de manter a ROM padrão com apps; a comparação de riscos pode favorecer essa opção sobre uma ROM customizada. | Ausente. A fonte pede estudar ROMs existentes e integrar IA mais profundamente, mas não afirma nem mede esses riscos relativos. | `MODEL_HYPOTHESIS`; no JSON era `ontology_state=CANDIDATE`, mas a justificativa foi renderizada sem qualificação factual. |
| B | `candidate_possibilities[1].justification`: “Permite algumas automações e recursos de IA com menor risco que modificar a ROM completa.” | Justificar o launcher como caminho de menor risco. | Ausente; nenhuma comparação de risco foi fornecida ou verificada. | `MODEL_HYPOTHESIS`; candidato exploratório cuja justificativa aparecia como frase declarativa. |
| C | `candidate_possibilities[1].justification`: “Criadores costumam organizar ideias manualmente, mas o processo consome tempo e depende da criatividade individual.” | Diferenciar o SaaS de organização manual e sustentar valor/eficiência do produto. | Ausente. A fonte pede uma ferramenta de ideias e potencial de engajamento; não descreve práticas comuns, tempo gasto ou dependência de criatividade dos criadores. | `MODEL_HYPOTHESIS`; também repetido em trade-offs (“Consome tempo”, “Depende de criatividade individual”), todos sem suporte rastreável. |

No caso C, o refinamento também especificou “análise de tendências públicas do
TikTok” e algoritmos como mecanismo. Isso era uma proposta de mecanismo do
sistema, não evidência sobre disponibilidade, predição ou eficácia; permanece
hipótese e não foi usado para ampliar o bloqueio principal.

### Rastro de geração a apresentação

1. A resposta do modelo entra em `LeanFirstPassOutput.competing_alternatives`,
   cujos itens carregam `mechanism`, `justification`, `tradeoffs` e uma base
   alegada que por padrão é `MODEL_HYPOTHESIS`.
2. `EarlyEpistemicGate.evaluate` verifica a elegibilidade de autoridade do
   mecanismo para gates. Uma hipótese continua sendo candidata sem autoridade
   de gate; esse estágio não classifica cada oração factual da justificativa ou
   dos trade-offs.
3. `EvolutionArtifactMapper.map_lean_result` preserva a base como
   `MODEL_HYPOTHESIS`/`CANDIDATE` e copia justificativa e trade-offs sem
   reescrevê-los.
4. `cli.main` envia o artefato a `HumanResultRenderer.render`. Antes de RQ-09,
   esse renderizador mostrava o cabeçalho genérico de alternativas exploratórias,
   mas imprimia mecanismo, justificativa e trade-offs sem consultar
   `cand.authority_basis`. Assim, a proveniência estruturada correta se perdia
   na camada visível ao usuário.

**Root cause:** falha de propagação de status na apresentação, não promoção de
autoridade pelo gate. A proveniência existia no artefato; o renderizador a
ignorava precisamente nos candidatos comparativos em que o modelo colocava
claims externos dentro de frases factuais.

## Mudança mínima

Arquivos intencionais:

- `src/idea_evolution/rendering/human_result.py` — para cada
  `MODEL_HYPOTHESIS`, apresenta uma nota explícita de que mecanismo, justificativa
  e compensações não foram verificados e não devem ser lidos como fatos.
- `tests/test_rq09_epistemic_claim_boundary.py` — sete regressões determinísticas
  cobrindo os padrões e as invariantes solicitados.
- `docs/evidence/FIOIDEIAS-V1.1-RQ-09-EPISTEMIC-CLAIM-BOUNDARY.md` — este recibo.

O teste RQ-08 B conserva literalmente a frase sobre risco de ROM; o teste RQ-08 C
conserva literalmente a frase sobre organização manual e tempo. Ambos exigem a
qualificação visível. Testes separados verificam claim técnico externo, fato
explicitamente declarado pelo usuário, interpretação derivada válida,
possibilidade criativa e não acionamento dos gates RQ-07 por hipóteses do modelo.

## Verificação determinística

TESTE DIRECIONADO INICIAL (antes da mudança): 5 falhas / 2 passes; as falhas
incluíam ausência do status explícito nos dois padrões RQ-08.
TESTE DIRECIONADO APÓS A MUDANÇA: 7 passed.
SUÍTE COMPLETA: 529 passed, 1 warning, em 14.78s. Baseline antes dos sete novos
testes: 522 passed.
AVISO: um `PytestCollectionWarning` já conhecido para a classe Pydantic
`TestabilityBinding` em `src/idea_evolution/domain/evidence_boundary.py:87`, ao
coletar `tests/adversarial/test_adversarial_idea_ecology.py`. Nenhuma falha.

Casos cobertos:

1. `MODEL_HYPOTHESIS_IN_ALTERNATIVE_JUSTIFICATION`
2. `MODEL_HYPOTHESIS_IN_VALUE_REASONING`
3. `TECHNICAL_EXTERNAL_CLAIM_WITHOUT_EVIDENCE`
4. `USER_EXPLICIT_FACT_PRESERVED`
5. `VALID_DERIVATION_PRESERVED`
6. `CREATIVE_HYPOTHESIS_ALLOWED`
7. `RQ07_GATE_INVARIANTS`

O sétimo teste mantém hipótese do modelo inelegível para escalação normativa e
de vulnerabilidade, e mantém uma ação de modelo inelegível para gate. A suíte
completa também reexecuta as regressões existentes de contradição de input,
derivação e autoridade RQ-07. Não foi alterada a implementação desses gates.

## Known regression A/B/C — não cega

Os inputs foram executados novamente como regressões conhecidas. Seus SHA-256
continuam idênticos aos registrados em RQ-08; isto não é evidência cega, nova
generalização nem pontuação de release. Cada run fez uma chamada lógica e
terminou com `RETURN_NOW` / `escalation_reason=NONE`.

| Caso | Input SHA-256 | Run RQ-09 | SHA-256 de `final.md` | Verificação focal |
|---|---|---|---|---|
| A | `361E516C8C31CCDBA102A135BE9BC7E5E74B7F648CDDBDB9480C56C92F127794` | `RUN-20260930_122821` | `C19706CAE53E2D2BC0A0943ACA081FED63E2DFF1AE157E5E19F0ECBB293E5FC4` | Alternativas geradas aparecem com status não verificado; sem padrão focal de factualização de B/C. |
| B | `C9EB6C8E271D259E435DAE779BEA74B7B82CD6CBEA0A05115256CEC392D30DFE` | `RUN-20260930_122833` | `8BFE8E544C120CF5D4BD6DE834AB9939DF9DB35576FB959442D5FC0C7AC504C3` | Justificativas comparativas continuam exploráveis, mas são explicitamente marcadas como não verificadas. |
| C | `4C740A4C16B82298E1D1F85DB7ECC723B6E319C5D9A89B94B9A5F7084C77EB49` | `RUN-20260930_122843` | `45167BC3115FE0D4D24BDD2A492389482F12D5675ADB339ACAC3FEBAEDD7698E` | A afirmação de prevalência (“método atualmente usado por muitos criadores”) e trade-offs de tempo/criatividade estão sob o status explícito de hipótese não verificada. |

Artifacts initially preserved in `runs/RUN-20260930_122821/`,
`runs/RUN-20260930_122833/` e `runs/RUN-20260930_122843/` foram copiados sem
alteração para o arquivo externo registrado em
[FIOIDEIAS-V1.1-RELEASE-TREE-HYGIENE-ARCHIVE.md](FIOIDEIAS-V1.1-RELEASE-TREE-HYGIENE-ARCHIVE.md);
`final.md`, `evolution_artifact.json`, `final.json` e `input.json` foram conferidos
antes do arquivamento. Os
artefatos estruturados mantêm as alternativas como `MODEL_HYPOTHESIS`, os três
gates retornaram `RETURN_NOW` sem escalação, e nenhuma contradição de input foi
promovida. As ações finais de A/B/C são sugestões de produção de evidência
semanticamente relacionadas às respectivas ideias; o caso B pede a revisão de
ROMs já solicitada, e o caso C propõe validar a hipótese de engajamento. A
qualificação de status permanece explícita, não uma autorização de execução.

`authority_spoofing_detected=true` permaneceu nos metadados dos três runs,
embora não tenha alterado `RETURN_NOW` nem produzido escalação. O texto de
incertezas também ainda pode conter `SPOOFING_DETECTED` lexical para ações de
investigação. Isso permanece dívida/falso positivo conhecido do RQ-08 e não foi
alterado por esta correção, pois mexer no gate RQ-07 estava fora de escopo.

**Leitura do RQ-08 após a correção:** `MODEL_HYPOTHESIS_TRIGGERED_GATE=NO`;
`INPUT_CONTRADICTION_PROMOTED=NO`; `UNANCHORED_NEXT_ACTION=NO` na revisão
semântica dos três próximos passos. O marcador lexical `SPOOFING_DETECTED` ainda
pode aparecer em `EVIDENCE_NEEDED`, mas não é promoção de autoridade nem
acionamento de gate.

## Débito e limite da conclusão

- Persistem os falsos positivos lexicais `SPOOFING_DETECTED`, especificidade
  técnica não verificada em propostas e ausência de evidência externa vinculada
  oração por oração.
- O rótulo de RQ-09 opera por candidato inteiro. Ele preserva ideias e torna
  visível a incerteza, mas não certifica nem refuta cada proposição dentro do
  texto.
- `UNKNOWN != FALSE`, `POSSIBILITY != FACT`, `HYPOTHESIS != EVIDENCE` e
  `NOVELTY != TRUTH` continuam preservados.
- A/B/C agora são regressões conhecidas e nunca mais podem ser reportados como
  cegos. Um novo prospective blind test é necessário antes de qualquer alegação
  de generalização ou novo release gate; criar inputs ou iniciar tal gate está
  fora desta missão.

AUTHORITY_CHANGED=NO | RQ07_GATE_BEHAVIOR_CHANGED=NO
HOLDOUTS_ACCESSED=NO | REVEAL_ACCESSED=NO | TREATMENTS_CHANGED=NO
PRODUCT_ARCHITECTURE_REOPENED=NO

VERDICT=PASS_WITH_KNOWN_DEBT
NEXT_ALLOWED_STEP=STOP; novo prospective blind test somente sob missão humana separada
