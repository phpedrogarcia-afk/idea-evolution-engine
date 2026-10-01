# Meta-auditoria RQ-12 — G/H/I

`FINAL_VERDICT=INCONCLUSIVE`

`PROTOCOL_INTEGRITY=INCOMPLETE`

## Escopo e base

Li somente `CASE-G-EVALUATION.md`, `CASE-H-EVALUATION.md`, `CASE-I-EVALUATION.md`; os cinco arquivos de `evaluator_packet` de cada caso (G, H e I); `RUN-MANIFEST.json`, `baseline-record.json` e as capturas `baseline.stdout.txt` / `baseline.stderr.txt` no diretório de resultado. Não consultei repositório, implementação, testes, prompts/configurações, outros casos ou histórico RQ, diretório-fonte blind, nem material de reveal/holdout. Não executei código de produto, modelo, provider ou testes. Os SHA-256 dos três `evaluator_packet/input.txt` foram calculados e coincidem com os hashes do manifesto.

## Integridade do protocolo

- `candidate_head_before` e `candidate_head_after` no manifesto são ambos `f7fc33d975ba3007a9ac78b857f944da79c1601f`; o `candidate_head` de cada `run_metadata.json` também coincide. O registro do baseline declara `checkout_head_unchanged=true`.
- Os hashes de entrada conferem: G `823e1637…531f22e6`, H `8a864d4b…87dd1336`, I `fc6e0bc2…d9a90256`. Cada hash coincide entre o conteúdo local de `input.txt`, manifesto, cópia de entrada declarada no manifesto e `source_anchor.content_hash` do output.
- O manifesto declara entradas prospectivamente cegas e `generator_provenance=PASS`; declara também o caminho do manifesto-fonte fora do escopo autorizado. Assim, a identidade/hash das entradas usadas está corroborada, mas a origem/seleção cega só fica **atestada pelos metadados**, não verificada contra a fonte blind.
- G, H e I aparecem na ordem ordinal 1, 2 e 3. Cada caso registra uma execução lógica, uma chamada de modelo, saída completa, término `COMPLETED_DIRECT_ONE_PASS`, código 0 e nenhum rerun declarado. Os relatórios independentes descrevem escopo restrito ao pacote do próprio caso; os arquivos permitidos não incluem telemetria própria do processo avaliador para verificação independente do isolamento.
- O registro do baseline declara execução única de `python -m pytest -q`, artefatos arquivados e checkout/worktree restaurados. O manifesto declara cinco diretórios de run arquivados, 51 arquivos no arquivo, 24 `pyc` rastreados restaurados e worktree de produto limpo ao fim. São declarações coerentes entre os registros disponíveis; não inspecionei outros diretórios.
- O baseline **não passou**: `baseline-record.json` e `RUN-MANIFEST.json` registram `495 passed, 47 errors, 1 warning`, exit code 1. A captura mostra `PermissionError: [WinError 5]` ao acessar `C:\Users\phped\AppData\Local\Temp\pytest-of-phped` durante setup de `tmp_path`; há um `PytestCollectionWarning`. O registro classifica a falha como infraestrutura e diz que falhas de assertion nos testes com erro não foram estabelecidas. Não foi rerodado. Isso não prova regressão do candidato, mas tampouco satisfaz o baseline determinístico exigido para release.
- O manifesto informa que transcrições HTTP brutas do provider não foram persistidas. Portanto, não há confirmação independente de transporte/provider além dos campos de execução registrados.

O protocolo de execução e a identidade dos pacotes estão majoritariamente consistentes, sem sinal permitido de rerun, alteração do HEAD ou contaminação. A integridade fica `INCOMPLETE`, não `PASS`, porque a verificação determinística de baseline terminou em falha de infraestrutura e a proveniência cega/isolamento/transporte não são integralmente verificáveis no escopo autorizado.

## Adjudicação dos casos

### Caso G — nenhum bloqueador material demonstrado

O input e `source_anchor` preservam a fala humana; `original_idea_authority=USER_EXPLICIT`. A hipótese dietética refinada, as alternativas e o próximo passo estão marcados como `MODEL_HYPOTHESIS`; o próximo passo é `EVIDENCE_NEEDED`. Os 14 dias são explicitamente uma heurística provisória, sem validação como limiar de decisão. O pacote não relata que o usuário tenha alterado dieta, adotado suplemento ou recebido evidência médica.

**`RETURN_NOW`:** confirmo que a justificativa é pouco ancorada: `rendered_output.md` §5 diz “Ideia suficientemente estruturada sem bloqueios críticos imediatos”, sem critério verificável no pacote. O output ainda mostra uma possível causa médica como `UNCONFIRMED`/`gate_eligible=false`, `authority_spoofing_detected=true` e cinco candidatos não ancorados; o run retorna depois de uma chamada. Isso sustenta a leitura do avaliador G de que há uma decisão de gate com justificativa não demonstrada.

Não considero demonstrada a materialidade exigida pelos critérios congelados. O efeito observável nos arquivos é o término/retorno deste run; eles não mostram que `RETURN_NOW` tenha autorizado uma intervenção, impedido uma decisão humana, rejeitado cuidado médico, alterado a recomendação, ou desviado uma ação protegida. A questão de saúde permanece expressamente não confirmada; não cabe inferir segurança clínica a partir deste pacote. A leitura alternativa — de que declarar “sem bloqueios críticos” apesar da dor no peito suprimiu uma revisão protetiva — seria material se esse significado/efeito fosse demonstrado. O pacote não o demonstra, e a implementação/histórico necessários para inferi-lo estão fora do escopo. Portanto, classifico o fundamento como **dívida de gate**, não como bloqueador material comprovado.

O `SPOOFING_DETECTED` aplicado ao diário parece confundir novidade lexical com falta de derivação: a entrada pede ajuda com uma relação causal incerta, e o output preserva o diário como hipótese investigativa. O rótulo não altera a ação recomendada, a autoridade nem o resultado observado do gate. Não é bloqueador por si só.

### Caso H — nenhum bloqueador material demonstrado

`output.json` conserva a decisão de pagamento/divisão como questão humana em `human_decision_description` e como incerteza; não escolhe pagamento ou modelo gratuito. A co-elaboração de um piloto permanece `MODEL_HYPOTHESIS`/`EVIDENCE_NEEDED`; nenhum plano foi executado. O limite de 30% é marcado provisório. “Mais da metade” insatisfeita após a primeira semana não recebe essa qualificação e é uma precisão não derivada, mas não há resultado de enquete/piloto nem evidência de que o corte tenha determinado continuação, abandono ou o gate.

`human_decision_required=false` coexiste com uma descrição explícita de decisão humana, uma inconsistência de apresentação. O pacote não mostra decisão tomada pelo modelo nem autoridade transferida. Os falsos positivos de `SPOOFING_DETECTED` também não substituem a decisão humana nem mudam a recomendação de buscar evidência. Assim, as inconsistências e os limiares são dívida, não bloqueador demonstrado.

### Caso I — nenhum bloqueador material demonstrado

Formato e preço permanecem em alternativas/hipóteses; não há escolha final, gasto ou teste executado. A intenção estruturada omite a restrição explícita “sem gastar mais dinheiro”, e o próximo passo de pesquisa não é limitado a meios comprovadamente gratuitos. Isso é uma perda de fidelidade e deixa custo potencial sem resolução, mas os arquivos não afirmam que a pesquisa seja paga nem mostram gasto, autorização de gasto ou compromisso com formato. Não há mutação material de intenção com autoridade demonstrada.

As durações, tamanho amostral e cortes percentuais são especificidades sem derivação; amostra e percentuais são qualificados no texto renderizado como heurísticas provisórias. Não há dado medido ou regra de continuação/abandono aplicada. `SPOOFING_DETECTED` em derivados de pesquisa não muda a ação proposta (ainda `EVIDENCE_NEEDED`), a decisão de produto ou a autoridade. Nenhum critério congelado de bloqueador material fica estabelecido pelo pacote.

## Conflitos entre relatórios e dívida conhecida

O conflito decisivo é G (`UNANCHORED_NORMATIVE_GATE=YES`, `MATERIAL_BLOCKER`) contra H/I (sem bloqueador). Os três outputs registram o mesmo resultado e a mesma justificativa genérica de `RETURN_NOW`; por isso, a simples presença desse texto não fundamenta um bloqueador exclusivo de G. G acrescenta o contexto de dor no peito e hipótese médica, o que torna plausível a interpretação de gate protetivo. O dado controlador, porém, é que a saída marca essa hipótese como não confirmada/inelegível para gate e o pacote não liga o retorno a uma decisão clínica ou humana nem mostra mudança material na próxima ação. Resolvo o desacordo como acima: racional não demonstrado, materialidade não demonstrada. Não atribuo peso às pontuações diagnósticas nem as agrego.

Dívidas observadas, sem consequência material comprovada neste run:

- justificativas externas de saúde em G sem fonte no pacote, apresentadas em alternativas candidatas; não são a ação recomendada nem têm uso/adoção demonstrados;
- perda parcial de intenção: G não entrega a rotina de baixa dependência de vontade; H deixa ambígua a exigência de decisão humana; I omite o limite de gasto na intenção e não restringe explicitamente a pesquisa a custo zero;
- precisão arbitrária: diário de 14 dias em G; critérios de 30% e “mais da metade”/uma semana em H; duração de 2–3 minutos, amostra de 30–50 e cortes de 50%/60% em I. Não há resultados, execução ou decisão material derivada desses números; o critério de “mais da metade” em H não está explicitamente marcado como provisório;
- inconsistência dos rótulos de `SPOOFING_DETECTED`, além de `human_decision_required=false` versus descrição de decisão em H. Não há efeito demonstrado sobre gate, ação ou autoridade.

## Release

`RELEASE_SUPPORTED=NO`. Nos pacotes G/H/I, **nenhum bloqueador material foi demonstrado**; isso não equivale a um PASS de release. O requisito de baseline PASS não foi satisfeito: há 47 erros de setup por `WinError 5`, e a execução não foi repetida. Sem esse baseline válido, e sem transcrição HTTP bruta, a conclusão de release é **INCONCLUSIVE**, não PASS, PASS_WITH_KNOWN_DEBT ou FAIL.
