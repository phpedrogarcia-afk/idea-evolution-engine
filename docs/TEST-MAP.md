# TEST-MAP.md — Mapa da Suíte de Testes Automatizados (v0.2)

> **ESTRUTURA DE TESTES, COBERTURA DE RISCOS E EXECUÇÃO DETERMINÍSTICA.**
> *Total de Testes: 49 testes distribuídos em 10 módulos (100% automatizados e offline).*

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
| **Loop E2E** | `tests/integration/test_simple_loop_e2e.py` | 1 | Integração (<50ms) | Execução sequencial completa dos 6 estágios, gravação de artefatos em `runs/` e integridade do trace. |
| **Reconstrução** | `tests/integration/test_reconstruction_path.py` | 2 | Integração (<50ms) | Acionamento de reconstrução em caso de rejeição e prevenção de loop infinito (max 1 ciclo). |
| **Critique-Revision** | `tests/integration/test_critique_revision_loop.py` | 1 | Integração (<50ms) | Execução correta da topologia iterativa de 9 estágios da Condição C. |
| **Multi-Model E2E** | `tests/integration/test_multi_model_e2e.py` | 2 | Integração (<50ms) | Transporte de estado entre múltiplos provedores simulados, proveniência em disco e 9 estágios. |
| **Adversarial MVP** | `tests/adversarial/test_adversarial_mvp.py` | 3 | Adversarial (<50ms) | Ataques de schema corrompido, parada ruidosa (*fail-closed*), detecção de *essence drift* e injeção. |
| **Adversarial Multi-Model** | `tests/adversarial/test_adversarial_multi_model.py` | 4 | Adversarial (<50ms) | Anti-sequestro de rotas, isolamento de segredos, isolamento de falhas sem fallback silencioso. |
| **Experimento A/B/C** | `tests/experiment/test_comparison_packet.py` | 1 | Experimental (<50ms) | Execução sobre as 3 fixtures padronizadas e geração do pacote de avaliação cega mascarado. |

---

## ⚡ Como Executar Todos os Testes

```bash
# Executar a suíte completa de 49 testes
python -m unittest discover -s tests -p "test_*.py" -v

# Executar validação de contexto e integridade documental
python tools/context/validate_context.py

# Executar validação da arquitetura de inteligência
python tools/intelligence/validate_intelligence.py
```
