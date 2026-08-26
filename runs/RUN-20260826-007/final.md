# Pacote de Maturação da Ideia — Run RUN-20260826-007

**Status:** `REFINED_IDEA_READY` | **Ciclos de Reconstrução:** 0

---

## 1. Ideia Original (Imutável)

> Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Ajudar seres humanos a transformar ideias cruas em hipóteses acionáveis sem perda de intenção.
- **Problema Central:** Dificuldade do usuário em organizar e maturar ideias dispersas de forma estruturada.
- **Atores / Usuários:** Criadores, Engenheiros, Pesquisadores


## 3. Versão Refinada e Mecanismo Proposto

Idea Evolution Engine (Simple Loop): Motor sequencial CLI que recebe uma ideia humana crua, submete a 6 estágios dirigidos, valida esquemas e devolve um pacote de maturação estruturado com rastreabilidade total.


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Risco de sobrecarga de tokens e latência excessiva se o loop não tiver condições de parada estritas.
   - *Impacto:* Pode inviabilizar o custo por ideia processada.
   - *Parte Afetada:* Orquestração e limites de ciclo
2. **[MEDIUM]** Críticas podem se tornar genéricas se os prompts não impuserem Truth Over Agreement.
   - *Impacto:* Reduz o Decision Delta e gera valor perceptual ilusório.
   - *Parte Afetada:* Prompts de ataque


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Executar pipeline sequencial determinístico com contratos estritos Pydantic.
   - *Tradeoffs:* Menor flexibilidade dinâmica em favor de 100% de previsibilidade.
2. **Mecanismo:** Utilizar um único modelo com prompt estruturado em múltiplas seções.
   - *Tradeoffs:* Menor isolamento de contexto e menor severidade crítica.


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Modo de auditoria interativo com checkpoints gráficos no terminal.
2. *[CANDIDATE]* Suporte a plugins de exportação para ferramentas de issue tracking.


## 7. Propostas Rejeitadas (com Justificativa)

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
