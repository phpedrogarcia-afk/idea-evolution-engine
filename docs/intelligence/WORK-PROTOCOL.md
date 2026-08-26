# docs/intelligence/WORK-PROTOCOL.md — Protocolo Canônico de Trabalho de Agentes

> **O CICLO OPERACIONAL E EPISTEMOLÓGICO PADRÃO PARA QUALQUER IA NO IEE.**
> *Inteligência não é prosa; é a execução disciplinada deste protocolo.*

---

## 🔄 O Ciclo Canônico em 12 Etapas

```text
[1. ORIENT]        Ler AI-START-HERE, CURRENT-STATE, checkpoints, Git state.
       ↓
[2. CLASSIFY]      Classificar a tarefa (Mecânica, Semântica, Empírica, Normativa, Mista).
       ↓
[3. FRAME]         Definir o escopo, limites de contorno e restrições da tarefa.
       ↓
[4. RECON]         Inspecionar código/docs existentes; verificar se alguém já resolveu (Don't Reinvent).
       ↓
[5. HYPOTHESIZE]   Formular a hipótese explícita de mudança com baseline e condição de falha.
       ↓
[6. ATTACK]        Submeter a hipótese a crítica adversarial e desafio de simplicidade (Simplicity Challenge).
       ↓
[7. PLAN]          Elaborar plano de intervenção mínima estritamente no escopo autorizado.
       ↓
[8. ACT]           Executar a intervenção (proposta, código determinístico, doc ou teste).
       ↓
[9. VERIFY]        Validar via testes determinísticos, reprodução ou revisão por pares.
       ↓
[10. INTERPRET]    Interpretar o resultado sem exagero (distinguir possibilidade de confiabilidade).
       ↓
[11. RECORD]       Persistir achados em FINDINGS.md, decisões em DECISIONS-LEDGER.md e estado em CURRENT-STATE.md.
       ↓
[12. CHECKPOINT]   Emitir checkpoint imutável e validar integridade via validate_context.py.
```

---

## 📋 Detalhamento Operacional das Etapas

### 1. ORIENT (Orientação Obrigatória)
- Executar `python tools/context/project_status.py` ou ler [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md).
- Verificar o último checkpoint em [`docs/context/checkpoints/`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/).
- Confirmar correspondência entre o filesystem e o `context-manifest.json`.

### 2. CLASSIFY (Classificação)
- Identificar a natureza da tarefa conforme [`docs/intelligence/TASK-CLASSIFICATION.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/intelligence/TASK-CLASSIFICATION.md).
- Ajustar a estratégia de execução (ex: determinística para tarefas mecânicas, decomposição para mistas).

### 3. FRAME (Enquadramento)
- Identificar o `TaskContract` ou delimitar entradas, saídas esperadas e ações expressamente proibidas (`DO-NOT-DO`).

### 4. RECON (Reconhecimento e Anti-Redundância)
- Buscar no repositório se a solução, definição ou doador já existem (`Don't Reinvent Check`).
- Se houver gap externo concreto, executar *Donor Autopsy* orientada a gaps.

### 5. HYPOTHESIZE (Formulação de Hipótese)
- Estruturar a mudança no formato formal: `Problem`, `Baseline`, `Change`, `Expected Effect`, `Failure Condition`.
- Diagnóstico de modelo é hipótese, não fato, até ser verificado por evidência.

### 6. ATTACK (Ataque Adversarial e Simplicidade)
- Aplicar o *Simplicity Challenge*: "Existe uma intervenção mais simples que preserva o mecanismo central?".
- Testar contraexemplos mentais e pontos de falha antes de editar qualquer arquivo.

### 7. PLAN & 8. ACT (Planejamento e Ação Mínima)
- Conduzir a menor intervenção útil necessária.
- Modificar apenas arquivos dentro do escopo autorizado.

### 9. VERIFY (Verificação)
- Executar testes unitários, validações determinísticas e testes de regressão.
- Para bugs: *Reproduce First $\to$ Minimal Failing Test $\to$ Patch $\to$ Pass $\to$ Regression Check*.

### 10. INTERPRET (Interpretação e Honestidade)
- Registrar falhas com a mesma transparência que sucessos.
- Se nenhum avanço material for alcançado, emitir legitimamente `NO_USEFUL_WORK_FOUND`.

### 11. RECORD & 12. CHECKPOINT (Persistência e Fechamento)
- Atualizar `FINDINGS.md`, `CURRENT-STATE.md` e `ACTIVE-QUEUE.md`.
- Gerar checkpoint imutável via `python tools/context/create_checkpoint.py`.
- Rodar `python tools/context/validate_context.py` (deve retornar código 0).
