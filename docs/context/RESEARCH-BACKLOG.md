# docs/context/RESEARCH-BACKLOG.md — Backlog de Pesquisa Científica e Epistemológica

> **SEPARAÇÃO ESTRITA: O QUE PRECISAMOS SABER (RESEARCH) vs O QUE PRECISAMOS CONSTRUIR (BUILD)**
> Toda pesquisa deve responder a um gap receptor concreto, sem turismo tecnológico.

---

## 🔬 Linhas de Pesquisa Ativas (Things We Need To Know)

### 1. Pesquisa sobre Detecção Heurística de Saturação (Gap Receptor: ProgressMonitor)
- **Objetivo:** Estabelecer uma função de similaridade semântica para rejeitar propostas redundantes de LLM no bootstrap.
- **Doador Relacionado:** Magentic-One (Stall Detection).
- **Status:** `PLANNED`
- **Impacto:** Redução de até 40% no consumo de tokens em sessões de ideação.

### 2. Pesquisa sobre Tipagem Mínima de Atos Epistêmicos (Gap Receptor: DeliberationContract)
- **Objetivo:** Avaliar empiricamente se o conjunto de 8 atos (`FRAME`, `PROPOSE`, `CHALLENGE`, `GROUND`, `UPDATE`, `REFRAME`, `SYNTHESIZE`, `RECOMMEND`) cobre todas as interações necessárias sem a sobrecarga dos 14 atos do DCI.
- **Doador Relacionado:** DCI (Stanford).
- **Status:** `PLANNED`
- **Impacto:** Menor latência e maior fidelidade de seguimento de instruções pelos modelos.

### 3. Pesquisa sobre Oráculos de Teste para Hipóteses Não-Estatísticas (Gap Receptor: TestContract)
- **Objetivo:** Sistematizar métodos de teste para claims de usabilidade, viabilidade técnica e modelos de negócios.
- **Doador Relacionado:** POPPER (Falsificação Sequencial).
- **Status:** `PLANNED`
- **Impacto:** Conexão robusta entre a deliberação analítica e a realidade empírica de mercado.

---

## 🏗️ Linhas de Engenharia Separadas (Things We Need To Build)
*(Consultar a [`docs/context/ACTIVE-QUEUE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/context/ACTIVE-QUEUE.md) para a ordem autorizada de implementação)*
- Schemas formais JSON/Pydantic (`IdeaGenome`, `GenomePatch`, etc.).
- Validador determinístico do kernel (`GenomeValidator`).
- Pipeline sequencial do *Simple Idea Evolution Loop*.
