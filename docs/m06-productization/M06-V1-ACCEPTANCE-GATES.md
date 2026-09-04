# M06-V1-ACCEPTANCE-GATES.md — Portões de Aceitação e Critérios de Conclusão do FioIdeias V1

> **SISTEMA:** FioIdeias V1 — Lean L1 Default  
> **FASE:** M06 — Productization  
> **ESTADO:** `ALL_GATES_PASSED_RELEASE_READY`  
> **DATA:** 2026-09-04

---

## 1. Portões de Aceitação de Produto (V1 Exit Criteria)

A entrega da versão FioIdeias V1 exige o cumprimento estrito e verificável dos 12 portões de aceitação abaixo (todos auditados e aprovados na Fase P7):

| # | Portão de Aceitação | Critério Verificável | Método de Verificação | Status |
|---|---|---|---|:---:|
| **GATE-01** | **Entrada Estável Única** | Ideia crua aceita por um único comando canônico (`iee evolve -i "..."` ou `-f arquivo.txt`). | Teste de integração CLI. | **PASS** |
| **GATE-02** | **Execução Lean L1 Ponta a Ponta** | Execução nominal de 1 passada com avaliação determinística do Early Epistemic Gate a custo zero. | Teste de ponta a ponta com asserção de chamadas $= 1$. | **PASS** |
| **GATE-03** | **Escalação Focada Condicional** | Incerteza material dispara no máximo 1 chamada adicional focada ($2 \text{ chamadas máx}$). | Teste de cenário com severidade `HIGH` acionando escalação. | **PASS** |
| **GATE-04** | **Geração do Artefato Canônico** | Produção de `EvolutionArtifact` contendo todas as 9 dimensões contratuais de produto. | Validação estrita de schema Pydantic. | **PASS** |
| **GATE-05** | **Preservação de Proveniência** | Ancoragem criptográfica da entrada original (`SourceAnchor`) com ID e hash invariantes. | Verificação de hash `source_anchor.content_hash`. | **PASS** |
| **GATE-06** | **Fidelidade da Intenção Humana** | Intenção do usuário claramente expressa no resultado, sem desvios introduzidos pela IA. | Auditoria contra `SourceAnchor` e revisão textual. | **PASS** |
| **GATE-07** | **Separação Ontológica Estrita** | Fatos declarados pelo usuário (`USER_EXPLICIT`) não se misturam com hipóteses do modelo (`MODEL_CANDIDATE`). | Teste adversarial de spoofing com rebaixamento auditado. | **PASS** |
| **GATE-08** | **Tratamento Tipado de Erros** | Falhas de infraestrutura (429, 500) e validação mapeadas em estados limpos sem crashes ou dados corrompidos. | Testes de falha induzida e erro simulado. | **PASS** |
| **GATE-09** | **Garantia de Custo Zero de Bolso** | Sistema opera exclusivamente sob cotas gratuitas, bloqueando qualquer fallback pago (*fail-closed*). | Inspeção de rotas e política de billing nula. | **PASS** |
| **GATE-10** | **Zero Regressão na Suíte de Testes** | 100% dos testes determinísticos do repositório continuam passando ($\ge 332$ testes verdes). | Execução de `pytest` (445/445 passando). | **PASS** |
| **GATE-11** | **Validação em Ideias Reais Diversas** | Execução completa com sucesso em múltiplos tipos de ideias reais (ferramenta, negócio, produto). | Bateria de 8 casos reais E2E na Fase P7. | **PASS** |
| **GATE-12** | **Interface Humana Ergonômica e Limpa** | Saída legível e limpa em Markdown sem resíduos de debug, notas de experimento ou códigos internos de laboratório. | Inspeção visual do artefato final renderizado pelo `HumanResultRenderer`. | **PASS** |


---

## 2. Não-Objetivos Explícitos do FioIdeias V1 (Non-Goals)

Os seguintes tópicos estão **formal e expressamente fora do escopo** do FioIdeias V1:

1. ❌ **Ablação de Mecanismo Causal:** Não é necessário separar empiricamente a influência do prompt de primeira passada versus o Early Gate para entregar o V1.
2. ❌ **Continuidade do Programa M05 (M05.6):** A fase de exploração científica de provedores e validação confirmatória está formalmente encerrada.
3. ❌ **Reabilitação da Condição B (Simple Loop):** A Condição B permanece arquivada internamente e não será otimizada ou ajustada para o produto V1.
4. ❌ **Frameworks Multiagente e Enxames:** Proibido introduzir LangChain, AutoGen, CrewAI ou arquiteturas de enxame (*swarms*). O fluxo é puramente controlado por funções tipadas.
5. ❌ **Autoridade Autônoma de Implementação:** O IEE não escreve código produtivo no mundo real, não cria arquivos fora de sua árvore de runs e não executa comandos no sistema do usuário.
6. ❌ **Autoridade Operacional do FioOS:** O IEE não concede leases, não gerencia sandboxes e não toma decisões de execução governada.
7. ❌ **Interface Gráfica Complexa / Web App:** O V1 prioriza terminal (CLI) e artefatos em Markdown; interfaces web elaboradas ficam para versões futuras.
8. ❌ **Memória de Longo Prazo Complexa ou Base Vetorial Pesada:** A memória durável em V1 é baseada no histórico de runs locais e no artefato persistido, sem bancos vetoriais distribuídos.
9. ❌ **Marketplaces, Monetização ou Recursos Sociais:** Não há perfis de usuário, compartilhamento em nuvem ou modelos de cobrança.
10. ❌ **Infraestrutura Distribuída Desnecessária:** O motor permanece leve, autocontido em Python 3.10+ e executável localmente.
