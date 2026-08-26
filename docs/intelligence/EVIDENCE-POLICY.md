# docs/intelligence/EVIDENCE-POLICY.md — Política Canônica de Evidência e Status Epistêmico

> **POLÍTICA DE RIGOR EPISTEMOLÓGICO, PROVENIÊNCIA E INDEPENDÊNCIA DE DADOS.**
> *Memória não é evidência; inferência de modelo não é fato.*

---

## 1. Tipologia Estrita de Evidência

Toda informação ou dado registrado no `evidence_registry`, em relatórios ou em findings deve ser classificado em um dos tipos:

| Tipo de Evidência | Definição | Exemplo |
| :--- | :--- | :--- |
| **`FACT`** | Dado empiricamente comprovado, reproduzível e incontroverso no domínio. | Execução de script determinístico retornou código 0. |
| **`OBSERVATION`** | Medição ou dado bruto observado diretamente sem generalização causal. | Modelo X demorou 1.2s e consumiu 850 tokens na fixture Y. |
| **`EXPERIMENT_RESULT`** | Resultado obtido através de protocolo controlado com baseline e métrica formal. | Teste EXP-001 demonstrou que contratos reduziram redundância em 38%. |
| **`SOURCE_CLAIM`** | Afirmação extraída de artigo, documentação externa ou paper de terceiro. | "Autores do DCI alegam que múltiplos agentes aumentam nuance deliberativa." |
| **`MODEL_INFERENCE`** | Raciocínio, extrapolação ou síntese gerada probabilisticamente por LLM. | "Este componente plausivelmente falhará sob concorrência alta." |
| **`DESIGN_HYPOTHESIS`** | Suposição de design nossa a ser verificada no projeto. | "O validador em 5 camadas impedirá mutações não autorizadas." |
| **`HUMAN_DECISION`** | Declaração soberana do criador humano sobre valores, propósito ou restrições. | "O foco do projeto não deve ser um gerador automático de startups." |
| **`SPECULATION`** | Possibilidade teórica aberta sem sustentação empírica presente. | "No futuro, MCTS pode otimizar topologias deliberativas." |

---

## 2. Taxonomia de Status Epistêmico

Obrigatória em documentos de pesquisa e autópsias de doadores:
- **`CONFIRMED`:** Sustentado por execução de código, teste comprovado ou prova formal.
- **`PLAUSIBLE`:** Coerente e logicamente consistente, mas ainda não verificado no repositório.
- **`BORROWED_MODEL`:** Conceito adaptado de sistema ou autor externo.
- **`DESIGN_HYPOTHESIS`:** Proposta de engenharia nossa submetida a teste.
- **`SPECULATION`:** Ideia exploratória sem validação.
- **`REFUTED`:** Hipótese testada e derrubada experimentalmente.
- **`REJECTED`:** Avaliada e descartada por incompatibilidade ou violação de invariantes.
- **`UNKNOWN`:** Estado de ignorância declarado e investigável.

---

## 3. Independência de Fontes: Modelo Não É Fonte Independente
> **Três modelos de IA concordando com a mesma afirmação NÃO constituem três evidências independentes.**

Modelos de linguagem compartilham corpus de treinamento, vieses de alinhamento e estruturas probabilísticas semelhantes.
Para avaliar independência factual, o sistema deve rastrear:
1. `source_family`: Provedor / Origem dos dados primários.
2. `method_family`: Metodologia de coleta (benchmark, dedução formal, teste empírico).
3. `data_origin`: Dados brutos utilizados no experimento.
4. `model_family`: Arquitetura do modelo (ex: GPT vs Claude vs Gemini vs Llama).
