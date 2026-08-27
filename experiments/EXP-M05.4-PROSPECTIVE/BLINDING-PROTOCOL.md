# BLINDING-PROTOCOL.md — Protocolo de Cegamento e Prevenção de Vazamento M05.4

> **PROTOCOLO DE INTEGRIDADE EXPERIMENTAL**
> **STATUS:** `FROZEN_BEFORE_EXECUTION` | `HASH_COMMITTED`

---

## 1. Eliminação de Vazamento de Metadados

Para corrigir as falhas observadas em M05.2 (onde identificadores e metadados de execução revelaram a condição B), o protocolo M05.4 impõe um processo determinístico de desidentificação de pacotes de avaliação:

### 1.1 Itens Terminantemente Proibidos no Pacote de Avaliação Humana
- ❌ Identificadores de condição (`COND-A`, `COND-B`, `COND-C`);
- ❌ Nomes de arquiteturas (`Baseline`, `Simple Loop`, `Lean IEE`, `FioED`);
- ❌ Run IDs e timestamps de execução com sufixos identificadores;
- ❌ Nomes de estágios de pipeline (`01_UNDERSTAND`, `02_ATTACK`, etc.);
- ❌ Contadores de chamadas de modelo e telemetria de latência/tokens;
- ❌ Nomes de provedores ou modelos (`Groq`, `gpt-oss-120b`).

---

## 2. Envelope de Apresentação Padronizado

Todos os resultados serão formatados estritamente sob o seguinte template uniforme:

```markdown
# PACOTE DE AVALIAÇÃO CEGA — [IDEA_ID]

> **IDEIA ORIGINAL:** "[RAW_IDEA_TEXT]"

---

## RESULTADO 1
[CONTEÚDO NORMALIZADO DA EVOLUÇÃO]

---

## RESULTADO 2
[CONTEÚDO NORMALIZADO DA EVOLUÇÃO]

---

## RESULTADO 3
[CONTEÚDO NORMALIZADO DA EVOLUÇÃO]
```

---

## 3. Mapeamento Aleatorizado por Ideia e Compromisso Criptográfico

1. O mapeamento entre `RESULT_1`, `RESULT_2`, `RESULT_3` e as condições reais `CONDITION_A`, `CONDITION_B`, `CONDITION_C` varia de forma independente para cada uma das 8 ideias da suíte.
2. O arquivo de mapeamento [`BLIND-REVEAL.json`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/BLIND-REVEAL.json) foi gerado deterministicamente sob a semente `20260827`.
3. O hash SHA256 do arquivo de revelação está congelado e registrado publicamente em [`BLIND-REVEAL.sha256`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.4-PROSPECTIVE/BLIND-REVEAL.sha256) com valor:
   `970b03ad8eece795dea11653e744d1b4b3a2314f0e6db5bd883c307fa8ff97b4`.

---

## 4. Regra Inegociável de Abertura

1. O avaliador humano preencherá todas as notas e rankings no arquivo `M05.4-HUMAN-REVIEW.md`.
2. O arquivo de avaliação humana será salvo e terá seu hash SHA256 calculado (`HUMAN_REVIEW_FROZEN`).
3. **SOMENTE APÓS O CONGELAMENTO DA AVALIAÇÃO HUMANA** o arquivo `BLIND-REVEAL.json` será aberto e processado.
4. Qualquer abertura prematura do mapeamento anulará o experimento.
