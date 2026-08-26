# Pacote de Maturação da Ideia — Run RUN-20260826-002

**Status:** `REFINED_IDEA_READY` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um gerenciador de tarefas que prioriza por energia mental e nao apenas por horario.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Ajudar seres humanos a transformar ideias cruas em hipóteses acionáveis sem perda de intenção.
- **Problema Central:** Dificuldade do usuário em organizar e maturar ideias dispersas de forma estruturada.
- **Atores / Usuários:** Criadores, Engenheiros, Pesquisadores


## 3. Versão Refinada e Mecanismo Proposto

Idea Evolution Engine (Simple Loop): Motor sequencial CLI que recebe uma ideia humana crua, submete a 6 estágios dirigidos, valida esquemas e devolve um pacote de maturação estruturado com rastreabilidade total.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Crítica focada (CRITIQUE_1): Premissa de validação sem atrito precisa de teste empírico.
   - *Impacto:* Pode falhar em situações reais fora do laboratório.
   - *Parte Afetada:* Viabilidade operacional
2. **[HIGH]** Crítica focada (CRITIQUE_2): Premissa de validação sem atrito precisa de teste empírico.
   - *Impacto:* Pode falhar em situações reais fora do laboratório.
   - *Parte Afetada:* Viabilidade operacional


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Executar pipeline sequencial determinístico com contratos estritos Pydantic.
   - *Tradeoffs:* Menor flexibilidade dinâmica em favor de 100% de previsibilidade.
2. **Mecanismo:** Utilizar um único modelo com prompt estruturado em múltiplas seções.
   - *Tradeoffs:* Menor isolamento de contexto e menor severidade crítica.


## 6. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Adicionar banco de dados vetorial e interface gráfica web. (Origem: ALTERNATIVES)
  *Motivo:* Viola o princípio Simple Before Platform e expande desnecessariamente o escopo do MVP.


## 7. Dependências da Realidade & Testes Empíricos Necessários

**Dependências Externas:**
- Disponibilidade de chave de API para o modo real ou execução offline com mocks.

**Testes Discriminativos Sugeridos:**
- [ ] Executar teste cego A/B comparando o Simple Loop contra o prompt único sobre 3 fixtures padronizadas.
- [ ] Medir a taxa de conformidade de schema em 100 execuções sucessivas.


## 8. Próximo Passo Recomendado

Executar experimento EXP-M04-001 comparando a saída do loop com o baseline de prompt único.
