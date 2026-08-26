# MISSION-04: Simple Idea Evolution Loop MVP — TaskContract

> **CONTRATO FORMAL DE PLANEJAMENTO PARA A MISSÃO 04 (PRÓXIMO ALVO AUTORIZADO).**
> *Status: DRAFT PREPARED / AGUARDANDO AUTORIZAÇÃO HUMANA FORMAL.*

---

## 1. Identificação da Tarefa

- **task_id:** `MISSION-04-MVP-SIMPLE-LOOP`
- **objective:** Implementar o protótipo executável do **Simple Idea Evolution Loop** que automatiza o ciclo manual de transportar uma ideia humana entre funções dirigidas de IA, gerando uma representação refinada e testável com estado compartilhado estruturado.
- **why_now:** As três fundações (Constituição, Continuidade e Inteligência) estão completas. A aplicação do princípio *Reality Over Deliberation* exige que o próximo avanço de conhecimento venha da construção e teste do primeiro loop prático, em vez de mais discussões documentais.
- **target_uncertainty:** Demonstrar empiricamente se um pipeline heurístico sequencial de 6 estágios dirigidos é capaz de maturar ideias cruas sem dependência de orquestradores complexos ou frameworks multiagente.
- **target_decision:** Validar a viabilidade do Single Agent Pipeline antes de avaliar necessidade de DCE com múltiplos agentes.
- **expected_decision_delta:** `IMPLEMENTED_CAPABILITY`
- **task_type:** `IMPLEMENTATION`
- **risk_level:** `HIGH`
- **context_profile:** `IMPLEMENTATION_ENTRY`
- **required_sources:**
  - [`AI-START-HERE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AI-START-HERE.md)
  - [`docs/context/CONTINUITY-CAPSULE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CONTINUITY-CAPSULE.md)
  - [`docs/foundations/PROBLEM-DEFINITION.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/foundations/PROBLEM-DEFINITION.md)
  - [`docs/doctrine/OPERATING-DOCTRINE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/doctrine/OPERATING-DOCTRINE.md)
  - [`docs/intelligence/WORK-PROTOCOL.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/WORK-PROTOCOL.md)

---

## 2. Escopo Autorizado & Entregáveis

### 🟢 Authorized Scope:
- `src/idea_evolution/simple_loop/` (Pipeline heurístico do MVP).
- `schemas/simple_loop/` (Schemas JSON/Pydantic do estado mínimo compartilhado).
- `tests/simple_loop/` (Testes unitários e fixtures de ideias em estado bruto).

### 🔴 Forbidden Scope (DO-NOT-DO):
- ❌ **NÃO** implementar RL, otimização de grafos MCTS ou aprendizado de topologia.
- ❌ **NÃO** criar dependência operacional ou acoplamento com o FioOS.
- ❌ **NÃO** implementar banco de dados relacional ou vetorial de produção.
- ❌ **NÃO** construir interfaces gráficas, dashboards web ou rotas HTTP complexas.
- ❌ **NÃO** criar personagens de roleplay antropomórfico (usar funções cognitivas diretas).

---

## 3. Especificação dos Estágios do Pipeline

```text
[Entrada: Raw Human Idea Text]
       ↓
[1. UNDERSTAND]      Extrai intenção, essência, problema e claims preliminares.
       ↓
[2. ATTACK]          Crítica adversarial severa; expõe premissas frágeis e falhas lógicas.
       ↓
[3. ALTERNATIVES]    Reconstrói opções e propõe mecanismos causais alternativos.
       ↓
[4. REALITY_CHECK]   Mapeia o que depende estritamente do mundo real e formula testes.
       ↓
[5. SYNTHESIZE]      Consolida a nova versão estruturada com tensões preservadas.
       ↓
[6. FINAL_REVIEW]    Verifica se restam inconsistências materiais não resolvidas.
       ↓
[Saída: REFINED_IDEA_PACKAGE ou CONTINUE/RECONSTRUCT]
```

---

## 4. Critérios de Aceitação e Evidência
1. O pipeline deve rodar localmente de ponta a ponta sobre 3 fixtures padronizadas (software, modelo de negócios e produto físico).
2. O estado compartilhado deve ser persistido em formato JSON estruturado e validável.
3. 100% dos testes unitários do pipeline devem passar em execução determinística.
4. Deve ser possível comparar o ganho de estrutura contra o baseline de prompt único (EXP-001).

---

## 5. Condição de Parada (Stop Condition)
A missão é concluída e deve parar quando o Simple Loop processar uma ideia crua, gerar o pacote de maturação sem erros e salvar o resultado, emitindo o checkpoint `CP-YYYYMMDD-NNN`.
