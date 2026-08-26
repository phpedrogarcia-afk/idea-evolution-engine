# PRINCIPLES.md — Princípios Constitucionais e Metodológicos

> Este documento consolida os princípios herdados do ecossistema FioOS e os princípios epistemológicos próprios do **Idea Evolution Engine (IEE)**.

---

## 1. Princípios Herdados do FioOS (Regras Fundacionais)

1. **Não reinventar a roda:** Pesquise doadores e literatura antes de criar abstrações.
2. **Donor autopsy primeiro:** Estude mecanismos que falharam ou venceram em projetos anteriores.
3. **Extrair mecanismos, não frameworks:** Adote apenas a engrenagem necessária, nunca o framework inteiro.
4. **Capability != Authority:** Capacidade técnica ou de raciocínio nunca confere autoridade soberana.
5. **Memory != Evidence:** Texto acumulado em contexto não é prova empírica.
6. **Context != Authority:** Injetar texto num prompt não confere direitos de mutação no sistema.
7. **Deterministic first:** Validações mecânicas, schemas e invariantes pertencem ao código determinístico; IAs atuam nas bordas semânticas.
8. **Failure is data:** Falhas de deliberação, rejeições e becos sem saída são dados científicos valiosos.
9. **Negative results remain data:** Evidência de inviabilidade não deve ser escondida ou descartada.
10. **Preserve contradictions:** Não suavize divergências lógicas ou empíricas por sínteses arbitrárias.
11. **Do not force consensus:** O consenso artificial mascara incertezas críticas.
12. **Baseline before improvement claim:** Toda alegação de avanço requer comparação formal com baseline.
13. **Prompts versioned:** Prompts e instruções são artefatos de código versionados e imutáveis.
14. **Policies versioned:** Critérios de promoção e transição de estado são políticas versionadas.
15. **Judge is an instrument:** O avaliador (humano ou LLM) é um instrumento de medição e requer calibração.
16. **One run proves possibility, not reliability:** Uma única execução bem-sucedida não prova robustez do protocolo.
17. **Reversibility:** Toda mutação relevante deve permitir reversão e auditoria de linhagem.
18. **Independent adversarial review:** A crítica deve ser executada por funções ou modelos desvinculados do proponente.
19. **Delegation transfers work, not authority:** Subagentes recebem tarefas delimitadas, nunca a soberania do criador.
20. **Bypassable boundary is not a boundary:** Fronteiras de segurança que podem ser contornadas por prompt não são fronteiras reais.
21. **Cost is part of experiment:** Custo computacional e de tokens é variável de controle essencial.
22. **Cheapest adequate model:** Utilize o modelo mais econômico capaz de executar a função epistemológica requerida.
23. **Autonomy grows with evidence:** A concessão de autonomia a agentes depende de comprovação empírica prévia.
24. **Stopping can be valid:** Encerrar ou arquivar uma ideia inviável é um resultado de sucesso do sistema.
25. **Persist state, not idle compute:** Persista o grafo estruturado imutável; não mantenha agentes rodando em loop ocioso.

> **Regra de Ouro do Ecossistema:**
> *"Dê aos agentes liberdade suficiente para nos surpreender, mas nunca liberdade suficiente para destruir nossa capacidade de estudar o que fizeram."*

---

## 2. Princípios Próprios do Idea Evolution Engine

1. **Progress over prose:** Aumento de volume de texto não é progresso; progresso é alteração de claim, evidência, premissa ou teste.
2. **Reality over deliberation:** Quando o próximo conhecimento de maior valor puder vir do mundo real, a deliberação cessa (`READY_TO_TEST`).
3. **Convergence without consensus:** O amadurecimento ocorre pelo mapeamento claro de acordos e desacordos, não por votação unânime.
4. **Human intent sovereignty:** O criador humano mantém o monopólio da intenção, dos *Protected Cores* e das decisões normativas.
5. **Evidence independence:** A repetição de uma afirmação por múltiplos modelos não aumenta sua independência estatística ou factual.
6. **Bootstrap is for structure, not decision:** No início, o sistema busca tornar a ideia legível (`StructureGain`), sem exigir relevância decisória prematura.
7. **Sparse genome is a regime, not a failure:** Um genoma inicial com poucos dados é um estado normal de bootstrap.
8. **Progress is contract-relative:** Critérios de sucesso devem ser formalizados no contrato *antes* da execução da rodada.
9. **Mixed questions must be decomposed:** Perguntas que misturam fatos e valores devem ser decompostas em frentes empíricas e normativas.
10. **Donor adoption must be gap-driven:** Nenhum sistema ou conceito externo é adotado sem uma lacuna receptora explícita.
11. **Human cognitive theory requires validation before AI transplantation:** Teorias cognitivas humanas (ex: TRIZ, C-K) não podem ser aplicadas cegamente a LLMs sem verificação empírica.
12. **Multi-agent is not default:** Deliberação multiagente só é autorizada quando houver alto valor de coordenação comprovado.
13. **Closure is not truth:** Encerrar uma rodada de deliberação significa apenas que o contrato terminou, não que a verdade absoluta foi atingida.
