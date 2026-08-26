# TEST-MAP.md — Mapa da Suíte de Testes Automatizados (v0.8)

> **ESTRUTURA DE TESTES, COBERTURA DE RISCOS E EXECUÇÃO DETERMINÍSTICA.**
> *Total de Testes: 86 testes distribuídos em 16 módulos (100% automatizados e offline).*

---

## 🗺️ Mapa de Módulos de Teste

| Módulo de Teste | Localização | Qtd | Tipo / Custo | O que Protege |
| :--- | :--- | :---: | :---: | :--- |
| **Continuidade** | `tests/continuity/test_continuity.py` | 7 | Determinístico (<10ms) | Entrada de novas IAs, integridade de manifestos e checkpoints, recuperação sem perda de estado. |
| **Inteligência** | `tests/intelligence/test_intelligence.py` | 10 | Determinístico (<10ms) | 10 cognitive traps bloqueados (Build Trap, Donor Trap, Evidence Trap, Baseline Trap, etc.). |
| **Doutrina** | `tests/doctrine/test_constitutional_doctrine.py` | 7 | Determinístico (<10ms) | Integridade de hash da Constituição v1.0, isolamento do FioOS, regras anti-círculo em contratos. |
| **Domínio e Estado** | `tests/unit/test_domain_state.py` | 4 | Unitário (<10ms) | Imutabilidade da ideia original, evolução em `current_idea`, registro de delta com proveniência. |
| **Contratos e Prompts** | `tests/unit/test_stage_contracts.py` | 2 | Unitário (<10ms) | Existência e integridade dos 10 arquivos de prompt, validação estrita de schemas Pydantic. |
| **Roteamento de Modelos** | `tests/unit/test_model_routing.py` | 5 | Unitário (<10ms) | Hash determinístico de config, falha ruidosa em alias/rota inválida, fallback de modelo único. |
| **Catálogo de Modelos & Custos** | `tests/unit/test_model_catalog.py` | 8 | Unitário (<10ms) | Rejeição de modelos encerrados, aplicação estrita de `FREE_ONLY`, exclusão de privacidade e regras de fallback. |
| **Fronteira IEE/FioOS (M06.2)**| `tests/unit/test_fioos_boundary_contracts.py` | 11 | Unitário (<10ms) | Invariantes de contrato: sem segredos no intent, READY_TO_TEST sem autoridade, transições ontológicas estritas. |
| **Loop E2E** | `tests/integration/test_simple_loop_e2e.py` | 1 | Integração (<50ms) | Execução sequencial completa dos 6 estágios na topologia corrigida (Synthesize -> RealityCheck), gravação e integridade de trace. |
| **Reconstrução** | `tests/integration/test_reconstruction_path.py` | 2 | Integração (<50ms) | Acionamento de reconstrução em caso de rejeição e prevenção de loop infinito (max 1 ciclo). |
| **Critique-Revision** | `tests/integration/test_critique_revision_loop.py` | 1 | Integração (<50ms) | Execução correta da topologia iterativa de 9 estágios da Condição C com Synthesize antes de RealityCheck. |
| **Multi-Model E2E** | `tests/integration/test_multi_model_e2e.py` | 2 | Integração (<50ms) | Transporte de estado entre múltiplos provedores simulados, proveniência em disco e 9 estágios. |
| **Adversarial MVP** | `tests/adversarial/test_adversarial_mvp.py` | 3 | Adversarial (<50ms) | Ataques de schema corrompido, parada ruidosa (*fail-closed*), detecção de *essence drift* e injeção. |
| **Adversarial Multi-Model** | `tests/adversarial/test_adversarial_multi_model.py` | 4 | Adversarial (<50ms) | Anti-sequestro de rotas, isolamento de segredos, isolamento de falhas sem fallback silencioso. |
| **Adversarial Catálogo & Custos** | `tests/adversarial/test_adversarial_catalog.py` | 4 | Adversarial (<50ms) | Injeção de modelos pagos sob `FREE_ONLY`, bloqueio de modelos descontinuados e integridade experimental no-fallback. |
| **Adversarial Essence Drift** | `tests/adversarial/test_adversarial_essence_drift.py` | 2 | Adversarial (<50ms) | Isolamento de *Speculative Feature Accretion* no Synthesis e acionamento de `RECONSTRUCT` no Final Review. |
| **Adversarial Understand & Groq** | `tests/adversarial/test_adversarial_understand_and_groq_boundary.py` | 3 | Adversarial (<50ms) | Pureza descritiva do UNDERSTAND, conformidade total com Groq Strict JSON Schema e preservação de `failed_generation`. |
| **Adversarial Ontologia, Alinhamento & Run ID (M05.1-R4)** | `tests/adversarial/test_adversarial_ontology_provenance.py` | 9 | Adversarial (<50ms) | Alinhamento do RealityCheck com o Core aceito, bloqueio de promoção circular (MODEL_HYPOTHESIS), 6 invariantes cross-state, e Run IDs imutáveis não reutilizáveis. |
| **Experimento A/B/C** | `tests/experiment/test_comparison_packet.py` | 1 | Experimental (<50ms) | Execução sobre as 3 fixtures padronizadas e geração do pacote de avaliação cega mascarado. |

---

## ⚡ Como Executar Todos os Testes

```bash
# Executar a suíte completa de 86 testes
python -m unittest discover -s tests -p "test_*.py" -v

# Executar validação de contexto e integridade documental
python tools/context/validate_context.py

# Executar validação da arquitetura de inteligência
python tools/intelligence/validate_intelligence.py
```
