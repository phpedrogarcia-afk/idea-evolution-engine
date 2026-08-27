# CURRENT-STATE.md — Estado Atual Real do Repositório

> **DECLARAÇÃO DE ESTADO REAL E FÍSICO DO REPOSITÓRIO.**
> *Para o snapshot operacional completo com branches, commits e checklist de tarefas ativas, consulte a casa canônica em [`docs/context/CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/CURRENT-STATE.md).*

---

## 1. Fase Ativa: Fase 1 — Simple Loop MVP & Experimento Real A/B/C Concluído
- **Status da Fundação:** `COMPLETE_AND_LOCKED` (`FOUNDATION_READY = TRUE`)
- **Status do Experimento A/B/C:** `A_B_C_EXECUTION_COMPLETE` (15 chamadas reais executadas contra Groq `openai/gpt-oss-120b`, zero fallback, R$ 0,00 incremental)
- **Status da Avaliação Humana:** `HUMAN_BLIND_REVIEW = PENDING` ([`experiments/EXP-M05.2-REAL/BLIND-REVIEW-PACKET.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.2-REAL/BLIND-REVIEW-PACKET.md))
- **Mapeamento Cego:** `ISOLATED_IN_BLIND_REVEAL_JSON` (Não revelado no relatório da IA)
- **Comparação Determinística:** [`experiments/EXP-M05.2-REAL/DETERMINISTIC-COMPARISON.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/experiments/EXP-M05.2-REAL/DETERMINISTIC-COMPARISON.md)
- **Status do MVP:** `IMPLEMENTED_AND_TESTED` (Software funcional, 114 testes verdes)
- **Branch Principal:** `main` | **Remote GitHub:** `https://github.com/phpedrogarcia-afk/idea-evolution-engine.git`
- **Varredura de Segredos:** `SECRET_SCAN: PASS`
- **Último Checkpoint Imutável:** [`CP-20260827-016`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/checkpoints/CP-20260827-016.md)

---

## 2. O que Existe Fisicamente no Repositório
- [x] Artefatos brutos da execução real em `experiments/EXP-M05.2-REAL/raw/` (`condition_a_raw.json`, `condition_b_raw.json`, `condition_c_raw.json`).
- [x] Pacote de avaliação cega em `experiments/EXP-M05.2-REAL/BLIND-REVIEW-PACKET.md`.
- [x] Arquivo de revelação isolado em `experiments/EXP-M05.2-REAL/BLIND-REVEAL.json`.
- [x] Comparação mecânica e determinística em `experiments/EXP-M05.2-REAL/DETERMINISTIC-COMPARISON.md` e `.json`.
- [x] Suíte de 114 testes automatizados e validadores de contexto 100% verdes.
