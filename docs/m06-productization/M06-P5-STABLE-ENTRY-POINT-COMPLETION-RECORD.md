# M06-P5-STABLE-ENTRY-POINT-COMPLETION-RECORD.md — Registro de Conclusão da Fase P5

> **PROGRAMA:** M06 — Productization  
> **FASE:** P5 — Stable User Entry Point / `iee evolve` $\to$ Lean L1  
> **STATUS:** `COMPLETE`  
> **DATA:** 2026-09-04  
> **INTEGRIDADE DO NÚCLEO CIENTÍFICO:** `LEAN_CORE_HASH_MATCH = YES` (`e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600`)  
> **CHAMADAS REAIS DE MODELO NA P5:** `0` (Custo de Bolso: `R$ 0,00` / `$0.00`)

---

## 1. Escopo e Objetivo da Fase P5

Estabelecer a interface de linha de comando estável e ergonômica para o **FioIdeias V1** (`iee evolve`), garantindo que:
1. **Ponto de Entrada Único e Canônico:** `iee evolve` é o comando oficial para usuários finais evoluírem ideias.
2. **Tratamento Padrão Lean L1:** A rota padrão incondicional é a **Condição C (Lean Loop L1 + Early Epistemic Gate)**, respaldada pela replicação experimental M05.5R2.
3. **Delegação Estrita à Camada de Serviço:** A CLI interage exclusivamente através de `IdeaEvolutionService.evolve()`, sem acessar diretamente classes internas de orquestração como `SimpleLoopRunner` ou `LeanLoopRunner`.
4. **Remoção do Legado de Pesquisa:** O loop de 6 estágios da Condição B foi completamente desacoplado do caminho padrão e despublicado da interface de usuário da CLI (`--condition-b`, `--simple-loop`, `--deep-loop`, `--topology` foram removidos do comando público `evolve`).
5. **Serialização do Artefato Canônico de Produto:** O resultado retornado pela CLI no modo `--json` é estritamente uma instância de `EvolutionArtifact` (v1.0), preservando proveniência ontológica completa.
6. **Distinção entre Desfecho de Domínio e Falha Operacional:** Estados deliberativos como `HUMAN_DECISION_REQUIRED` e `REFINEMENT_COMPLETE` são reportados com código de saída 0 (sucesso epistêmico), enquanto violações de contrato, rede ou limites operacionais retornam código 1.
7. **Salvaguarda de Custo Zero e Sanitização:** Aplicação rigorosa da política `ZeroCostGuard` (falha fechada para provedores desconhecidos ou tarifados) e sanitização total de segredos (`csk-***`, `Bearer ***`) na saída do terminal.
8. **Invariância Criptográfica do Núcleo Científico:** Preservação inviolável do hash SHA-256 combinado dos 7 arquivos congelados do Lean L1.

---

## 2. Inventário de Arquivos e Modificações

### Arquivos Criados:
- [`src/idea_evolution/cli/__init__.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/cli/__init__.py):
  - Inicialização limpa do pacote CLI sem importações circulares ou antecipadas.
- [`pyproject.toml`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/pyproject.toml):
  - Configuração moderna de empacotamento com script de console `iee = "src.idea_evolution.cli.main:main"`.
- [`iee.cmd`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/iee.cmd) e [`iee`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/iee):
  - Scripts executáveis de wrapper para chamadas imediatas em ambientes Windows e Unix (`./iee evolve "ideia"`).
- [`tests/test_fioideias_v1_cli.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/tests/test_fioideias_v1_cli.py):
  - Suíte completa de 20 testes determinísticos cobrindo todas as invariantes da Fase P5.
- [`docs/m06-productization/M06-P5-STABLE-ENTRY-POINT-COMPLETION-RECORD.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/m06-productization/M06-P5-STABLE-ENTRY-POINT-COMPLETION-RECORD.md):
  - Este registro formal de conclusão.

### Arquivos Modificados:
- [`src/idea_evolution/cli/main.py`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/src/idea_evolution/cli/main.py):
  - Reescrita completa do subcomando `evolve`: aceita argumentos posicionais `raw_idea` ou flags `--idea` / `--idea-file`.
  - Flags de controle de produto: `--fast` (contingência rápida), `--json` (emissão estruturada), `--provider`, `--model`, `--runs-dir`, `--dry-run`, `--debug`.
  - Remoção de flags da Condição B e do loop profundo experimental.
  - Roteamento exclusivo via `IdeaEvolutionService(runner=..., default_treatment=TreatmentMode.LEAN_L1)`.
  - Sanitização de credenciais em stdout e stderr via `sanitize_secret_text()`.
  - Saída tipada de erros com códigos de falha de serviço (`COST_POLICY_BLOCKED`, `PROVIDER_AUTH_FAILURE`, `PROVIDER_RATE_LIMIT`, `PROVIDER_SERVER_FAILURE`, etc.).
- Documentos de governança atualizados: `M06-V1-EXECUTION-PLAN.md`, `CURRENT-STATE.md`, `ACTIVE-QUEUE.md`.

---

## 3. Matriz de Invariantes da Fase P5

| Invariante | Requisito da Missão | Implementação Física | Status |
|---|---|---|:---:|
| `CLI_ENTRY_POINT_EXISTS` | `YES` | Comando `iee evolve` configurado via CLI (`src/idea_evolution/cli/main.py`) | **CONFIRMED** |
| `IEE_EVOLVE_WORKS` | `YES` | Execução síncrona/determinística validada por 20 testes unitários | **CONFIRMED** |
| `CLI_DEFAULT_TREATMENT` | `LEAN_L1` | Rota padrão incondicional é Condição C (Lean L1 + Early Epistemic Gate) | **CONFIRMED** |
| `CLI_USES_IDEA_EVOLUTION_SERVICE` | `YES` | `run_evolve()` instancia e despacha exclusivamente para `IdeaEvolutionService` | **CONFIRMED** |
| `CLI_BYPASSES_SERVICE` | `NO` | Zero invocações diretas de runners científicos a partir da CLI | **CONFIRMED** |
| `LEGACY_SIMPLE_LOOP_DEFAULT_REMOVED` | `YES` | `SimpleLoopRunner` removido do caminho do `evolve` | **CONFIRMED** |
| `CONDITION_B_PUBLICLY_EXPOSED` | `NO` | Flags `--condition-b`, `--simple-loop`, `--deep-loop`, `--topology` rejeitadas com exit 2 | **CONFIRMED** |
| `EXPERIMENTAL_DEEP_LOOP_PUBLICLY_EXPOSED` | `NO` | Nenhuma opção de loop de 6 etapas exposta na ajuda do `evolve` | **CONFIRMED** |
| `EVOLUTION_ARTIFACT_OUTPUT` | `YES` | Modo `--json` emite estritamente JSON válido de `EvolutionArtifact` v1.0 | **CONFIRMED** |
| `PROVENANCE_PRESERVED` | `YES` | `source_anchor`, `authority_class`, linhagem e ancoragens preservadas | **CONFIRMED** |
| `ZERO_COST_POLICY_PRESERVED` | `YES` | Validado via `ZeroCostGuard` e `CostEligibility` | **CONFIRMED** |
| `PAID_FALLBACK` | `NO` | Sem retries tarifados ou failover para modelos comerciais pagos | **CONFIRMED** |
| `DOMAIN_OUTCOME_DISTINCT_FROM_FAILURE` | `YES` | `HUMAN_DECISION_REQUIRED` emite exit code 0; falhas operacionais emitem exit code 1 | **CONFIRMED** |
| `SECRETS_IN_CLI_OUTPUT` | `NO` | Toda saída sanitizada contra chaves e tokens de provedores | **CONFIRMED** |
| `LIVE_MODEL_CALLS_DURING_P5` | `0` | 100% dos testes executados offline com fakes determinísticos | **CONFIRMED** |
| `OUT_OF_POCKET_COST` | `ZERO` | Custo de inferência = $0,00 | **CONFIRMED** |
| `LEAN_CORE_CHANGED` | `NO` | Hash combinado SHA-256 idêntico ao baseline de congelamento | **CONFIRMED** |

---

## 4. Auditoria de Testes

A suíte completa do repositório foi executada:
```
======================= 423 passed, 1 warning in 16.43s =======================
```
- **Testes dedicados de CLI P5:** 20/20 aprovados (`tests/test_fioideias_v1_cli.py`).
- **Testes de Governança de Provedores P4:** 20/20 aprovados (`tests/test_fioideias_v1_provider_guard.py`).
- **Testes de Proveniência Ontológica P3:** 20/20 aprovados (`tests/test_fioideias_v1_provenance_guard.py`).
- **Testes de Artefato de Evolução P2:** 20/20 aprovados (`tests/test_evolution_artifact.py`).
- **Testes de Limite de Serviço P1:** 11/11 aprovados (`tests/test_fioideias_v1_service_boundary.py`).
- **Testes Adversariais e Doutrinários:** 100% aprovados.

---

## 5. Verificação Criptográfica do Núcleo Científico

```
LEAN_CORE_HASH_BEFORE = e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600
LEAN_CORE_HASH_AFTER  = e6785bcaf5af291f438ab467386db640d4c0790e0f7012c40773dd25782e5600
STATUS                = STRICT_MATCH (ZERO MUTATION IN SCIENTIFIC CORE)
```

Os 7 arquivos canônicos congelados permaneceram 100% intocados:
1. `src/idea_evolution/domain/early_epistemic_gate.py` (`2bc13fdff123964f7b1e103ab52d41d61d7ca130eed07bdc1b7a0583063ebb62`)
2. `src/idea_evolution/domain/epistemic_contracts.py` (`639866dd801d8e60e93ce9ccb9d673c9df204a66a98c407c559a86adefc8e43b`)
3. `src/idea_evolution/domain/evidence_boundary.py` (`b75a369a0525dd2850b06d80d92add91a4acd71527f31ef8536328bced5e0a12`)
4. `src/idea_evolution/domain/grounding.py` (`d68c0598fa31c256d0e2ca1a3d01b11c0810c4f1330304cb5316a5397803733d`)
5. `src/idea_evolution/domain/state.py` (`9692daf65e3a4697b6847a1afb83a0231954cae564d726eae30c37b5dcfd0a83`)
6. `src/idea_evolution/orchestration/lean_loop.py` (`8e3551f87dc9c1b9a6bf225f96d6b50fe6bb48441eaa94e569438918fa6056d0`)
7. `src/idea_evolution/providers/base.py` (`24b49a58333d2ca9be8dc6dc01cf1749fecb91e9becd6e735bef4b61dc82ba02`)
