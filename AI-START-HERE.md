# AI-START-HERE

> **ESTE É O PONTO DE ENTRADA OBRIGATÓRIO PARA QUALQUER IA OU COLABORADOR.**
> Se você é uma IA iniciando uma nova sessão neste repositório, LEIA ESTE ARQUIVO PRIMEIRO antes de inspecionar qualquer código ou executar qualquer tarefa.

---

## 1. O que é o Idea Evolution Engine (IEE)
O **Idea Evolution Engine** é um sistema de investigação deliberativa que reduz, organiza e torna acionável a incerteza ao redor de uma intenção humana. Ele utiliza funções de IA, evidências externas, deliberação adversarial, memória epistêmica estruturada e validação determinística para amadurecer ideias sem transferir às máquinas a soberania sobre elas.

**Definição Operacional:** O sistema não recebe a missão genérica de “melhorar uma ideia”. Ele descobre o que precisa ser verdade, falso, conhecido ou testado para justificar o próximo passo racional daquela ideia.

---

## 2. O que o IEE explicitamente NÃO é (Antiobjetivos)
- **NÃO é um chat entre várias IAs** ou mesa-redonda de bots sem contrato.
- **NÃO é um conselho votando** para decidir por consenso se uma ideia é "boa".
- **NÃO é um gerador de startups** ou fábrica de pitches superficiais.
- **NÃO é um substituto do autor humano** (a IA propõe; o humano detém a soberania).
- **NÃO é um módulo interno do FioOS** (mantêm fronteira rígida de responsabilidades).
- **NÃO é um framework multiagente genérico** focado em quantidade de agentes.
- **NÃO é um sistema cuja qualidade é medida por tamanho de texto** (*Progress over Prose*).

---

## 3. Estado Atual: Fase 0 — Fundação / Bedrock
Estamos estritamente na **FASE 0 (FOUNDATION / BEDROCK)**.
Nesta fase, **NENHUM CÓDIGO DE PRODUTO É PERMITIDO**.

### 🚫 Ações Estritamente Proibidas Agora:
1. Criar aplicações web, mobile, UI, dashboards ou APIs REST/GraphQL.
2. Escrever orquestradores LLM reais, prompts de produção ou integrar SDKs de OpenAI/Claude/Gemini.
3. Criar classes mock/ornamentais vazias apenas para simular arquitetura.
4. Implementar bancos de dados de produção, autenticação, pagamentos ou infraestrutura cloud.
5. Iniciar qualquer implementação sem vínculo com a fila autorizada em [`docs/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/ACTIVE-QUEUE.md).

---

## 4. Ordem Obrigatória de Leitura
Para compreender a totalidade do projeto sem alucinar contexto:
1. [`AI-START-HERE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/AI-START-HERE.md) *(Você está aqui)*
2. [`docs/SOURCE-OF-TRUTH.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/SOURCE-OF-TRUTH.md) *(Hierarquia documental e epistemológica)*
3. [`docs/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/CURRENT-STATE.md) *(O que existe hoje vs o que é futuro)*
4. [`docs/GOVERNANCE-INVARIANTS.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/GOVERNANCE-INVARIANTS.md) *(Regras e restrições inegociáveis)*
5. [`docs/TERMINOLOGY.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/TERMINOLOGY.md) *(Glossário canônico)*
6. [`docs/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/ACTIVE-QUEUE.md) *(Trabalhos atualmente autorizados)*
7. [`docs/TARGET-ARCHITECTURE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/TARGET-ARCHITECTURE.md) *(Visão arquitetural alvo — não implementada ainda)*

---

## 5. Invariantes Constitucionais Não-Negociáveis
1. **Progress over prose:** Aumento de texto não é progresso. Progresso exige alteração em claim, evidência, premissa, incerteza decisiva ou teste real.
2. **Capability != Authority:** Uma IA mais inteligente não recebe soberania sobre a ideia. A intenção, valores e *protected cores* pertencem exclusivamente ao humano.
3. **Memory != Evidence:** Texto em histórico de chat ou suposição de LLM não é evidência. Toda evidência requer proveniência e tipagem.
4. **Deterministic First:** Validação estrutural, invariantes e transições de estado são 100% determinísticas no kernel; IA atua apenas nas bordas semânticas como proponente.
5. **LLM propõe; Kernel valida:** Nenhuma IA muta o `IdeaGenome` diretamente. Tudo entra via `GenomePatch` atômico validado pelo `GenomeValidator`.
6. **Reality over Deliberation:** Deliberação encerra quando um teste empírico no mundo real for a rota de maior valor informativo (`READY_TO_TEST`).
7. **Conversa não é processo:** Toda deliberação deve possuir um `DeliberationContract` prévio com critérios de parada, orçamento e definição estrita de progresso.
8. **Multi-agent is not default:** Se o valor de coordenação for baixo, o sistema deve operar em `SINGLE_AGENT_MODE`.

---

## 6. Diferença Crítica entre Status Documentais
Ao ler este repositório, você encontrará marcações epistemológicas:
- `CURRENT`: Realidade física e documental já aprovada e existente.
- `TARGET`: Arquitetura ou modelo planejado para fases posteriores.
- `RESEARCH` / `CANDIDATE`: Hipóteses, estudos de doadores ou ideias em avaliação.
- `CONFIRMED`: Mecanismo validado empiricamente.
- `DESIGN_HYPOTHESIS`: Suposição de design nossa aguardando teste.

> **REGRA DE OURO:** Jamais trate um arquivo de `TARGET` ou `RESEARCH` como se fosse código ou infraestrutura existente.

---

## 7. Como Propor Mudanças
1. Identifique um gap explícito ou consulte a [`docs/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/ACTIVE-QUEUE.md).
2. Não expanda escopo sem registrar decisão em [`docs/DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md).
3. Mantenha reversibilidade e rastreabilidade total.
4. Cada conceito possui uma única casa canônica (evite duplicação de definições).
