# M06-V1-ARCHITECTURE.md — Arquitetura de Produto do FioIdeias V1

> **SISTEMA:** FioIdeias V1 — Lean L1 Default  
> **FASE:** M06 — Productization  
> **ESTADO:** `FROZEN_FOR_IMPLEMENTATION`  
> **DATA:** 2026-09-03

---

## 1. Missão e Contrato do Usuário

O FioIdeias V1 é um serviço cognitivo com uma única missão bem delineada:

> *"Receber uma ideia crua e devolvê-la significativamente mais clara, criticada, contextualizada e refinada por meio de uma sequência controlada de funções de IA, preservando a intenção original e registrando o que mudou e por quê."*

### 1.1 Contrato de Entrada (Input Contract)
- **Entrada do Usuário:** Texto de ideia crua (string não estruturada ou arquivo `.txt`/`.md`).
- **Parâmetros Opcionais de Execução:**
  - `budget`: Custo máximo de chamadas (Default: 2, Teto Lean).
  - `fallback_mode`: Habilitação de fallback para Condição A em caso de timeout (`FAST_MINIMAL_REFINEMENT_FALLBACK`).
  - `export_format`: Formato de saída (`markdown`, `json`).

### 1.2 Contrato de Saída (Output Contract — EvolutionArtifact)
O produto retorna uma representação estruturada e auditável contendo:
1. **Ideia Original:** O texto literal e imutável fornecido pelo humano.
2. **Intenção Preservada:** O objetivo humano subjacente, isolado de detalhes acidentais de implementação.
3. **Ideia Refinada:** A formulação madura, clara e acionável.
4. **O Que Mudou:** O delta decisório concreto entre a entrada crua e a saída refinada.
5. **Críticas Importantes:** Vulnerabilidades materiais, pontos de fricção ou suposições frágeis.
6. **Premissas e Incertezas:** Suposições não verificadas e lacunas factuais remanescentes.
7. **Possibilidades Novas:** Alternativas técnicas ou conceituais viáveis propostas pelo sistema.
8. **Próximo Passo Recomendado:** Ação concreta imediata recomendada para o operador humano.
9. **Proveniência e Rotulagem Epistêmica:** Distinção visível entre fatos declarados pelo usuário e hipóteses sugeridas pelo sistema.

---

## 2. Diagrama de Fluxo e Componentes Arquiteturais

```
                                  HUMAN USER
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   User Entry Point (CLI)  │
                        │        iee evolve         │
                        └─────────────┬─────────────┘
                                      │
                                      ▼
                        ┌───────────────────────────┐
                        │   IdeaEvolutionService    │
                        │    (Application Layer)    │
                        └─────────────┬─────────────┘
                                      │
            ┌─────────────────────────┴─────────────────────────┐
            ▼                                                   ▼
┌───────────────────────┐                           ┌───────────────────────┐
│   ProviderAdapter     │                           │   LeanTreatmentCore   │
│  (Transport / Zero-   │                           │     (LeanLoopRunner)  │
│      Cost Guard)      │                           └───────────┬───────────┘
└───────────┬───────────┘                                       │
            │                                                   │
            │               1. LEAN FIRST PASS (Chamada 1)      │
            │◄──────────────────────────────────────────────────┤
            │──────────────────────────────────────────────────►│
            │                                                   │
            │               2. EARLY EPISTEMIC GATE (Custo 0)   │
            │               [Validação Determinística]          │
            │                                                   │
            │               3. Decisão do Gate:                 │
            │                  ├── RETURN_NOW ──────────────────┼──────┐
            │                  ├── REQUEST_HUMAN_DECISION ──────┼──────┤
            │                  └── ESCALATE_FOCUSED (Chamada 2) │      │
            │◄──────────────────────────────────────────────────┤      │
            │──────────────────────────────────────────────────►│      │
            │                                                          │
            │                                                          │
            │               4. Montagem do Artefato                    │
            │                                                          ▼
            │                                       ┌───────────────────────────┐
            │                                       │     EvolutionArtifact     │
            │                                       │ (Canonical Representation)│
            │                                       └─────────────┬─────────────┘
            │                                                     │
            │                                                     ▼
            │                                       ┌───────────────────────────┐
            │                                       │   HumanResultRenderer     │
            │                                       │   (Clean Markdown Output) │
            └───────────────────────────────────────┴───────────────────────────┘
```

---

## 3. Limites de Responsabilidade dos Componentes

### 3.1 `IdeaEvolutionService` (Camada de Aplicação)
- Coordena o ciclo de vida da requisição do usuário.
- Inicializa a ancoragem (`SourceAnchor`) e gera `run_id` rastreável.
- Seleciona o tratamento configurado (Default: `LeanTreatmentCore`).
- Gerencia exceções operacionais e invoca o renderizador final.

### 3.2 `LeanTreatmentCore` (Motor Científico Congelado)
- Executa a orquestração imutável de 2 chamadas máximas (`LeanLoopRunner`).
- Garante o acoplamento do `EarlyEpistemicGate` a custo zero de modelo.
- Assegura o fallback automático de autoridade para `MODEL_HYPOTHESIS` quando o modelo tentar alegar `USER_EXPLICIT` sem ancoragem.

### 3.3 `ProviderAdapter` (Camada de Transporte e Custo)
- Isola os SDKs de modelo do domínio de ideia.
- Aplica o guard inegociável de custo zero: se a cota gratuita esgotar ou a credencial faltar, emite erro tipado `PROVIDER_QUOTA_EXHAUSTED` ou `PROVIDER_AUTH_MISSING`, sem jamais chavear para provedores pagos.

### 3.4 `EvolutionArtifact` (Entidade Canônica de Estado de Produto)
- Estrutura de dados unificada que substitui a dispersão de dados de experimento.
- Combina `original_idea`, `interpreted_problem`, `primary_mechanism`, `vulnerabilities`, `delta` e `telemetria mínima de auditoria`.

### 3.5 `HumanResultRenderer` (Apresentação Limpa)
- Transforma o `EvolutionArtifact` em Markdown legível para seres humanos.
- Remove ruídos internos de laboratório: sem menção a Condições A/B/C, códigos de experimentos históricos (M05), tabelas de tokens de provedor ou logs de debug, a menos que o flag `--debug` seja solicitado explicitamente.

---

## 4. Modelo Tipado de Falhas Operacionais

O FioIdeias V1 adota separação estrita entre erros de infraestrutura, de domínio e de modelo:

| Tipo de Erro | Categoria | Causa Raiz | Comportamento do Sistema |
|---|---|---|---|
| **`PROVIDER_QUOTA_EXHAUSTED`** | Infraestrutura / Custo | Rate limit (429) ou cota diária esgotada no provedor free | Transição limpa fail-closed; notificação clara ao usuário sem retries infinitos. |
| **`PROVIDER_TRANSIENT_5XX`** | Infraestrutura | Erro temporário do servidor do provedor (500, 502, 503) | Replay idêntico único permitido se configurado; abortagem com preservação de estado se persistir. |
| **`SCHEMA_VALIDATION_ERROR`** | Domínio / Modelo | Saída do modelo inválida ou JSON corrompido | 1 tentativa de repair estruturado; falha limpa com preservação da ideia crua se falhar. |
| **`AUTHORITY_SPOOFING_INTERCEPTED`** | Epistêmico / Validação | Modelo tentou inventar fatos como sendo do usuário | Interceptação automática pelo validador determinístico; rebaixamento forçado para `MODEL_HYPOTHESIS`. |
| **`HUMAN_DECISION_REQUIRED`** | Negócio / Normativo | Dúvida de valor ético, político ou humano | Parada deliberada; devolução da opção ao humano sem inventar consenso artificial. |

---

## 5. Garantia Ontológica de Proveniência

Para assegurar que ideias sugeridas pela IA nunca se passem por intenção do usuário:

```yaml
PROVENANCE_LEVELS:
  CORE_USER_EXPLICIT:
    description: Fatos, restrições e objetivos expressos literalmente pelo humano.
    authority: MÁXIMA (Imutável pelo sistema).
  SYSTEM_DERIVED:
    description: Deduções analíticas estritas fundamentadas no input.
    authority: INFERIDA (Auditada pelo Gate).
  MODEL_CANDIDATE:
    description: Novas possibilidades, alternativas ou mecanismos sugeridos.
    authority: HIPOTÉTICA (Rotulada explicitamente como MODEL_HYPOTHESIS).
  REJECTED_PRUNED:
    description: Alternativas avaliadas e descartadas por inviabilidade ou contradição.
    authority: CONHECIMENTO NEGATIVO.
```

---

## 6. Fronteira de Integração com o FioOS

O FioIdeias V1 foi desenhado para manter total independência do FioOS, com interface preparada para o modo **`ADVISORY_SHADOW`**:

```
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│           FIOIDEIAS V1          │           │              FIOOS              │
│  - Serviço cognitivo de ideias  │           │  - Sistema Operacional          │
│  - Redução de incerteza         │  Futuro   │  - Sandboxing e Budgets         │
│  - Não executa comandos reais   ├──────────►│  - Leases de ferramentas        │
│  - Não cria arquivos externos   │  Advisory │  - Execução de tarefas reais    │
│  - Sem autoridade operacional   │           │  - Autoridade de execução       │
└─────────────────────────────────┘           └─────────────────────────────────┘
```
$$\mathbf{\text{IDEA } \ne \text{ REQUIREMENT } \ne \text{ TRUTH } \ne \text{ AUTHORITY}}$$
