# BOOTSTRAP.md — Regime Cognitivo de Estruturação

> **STATUS: TARGET / DESIGN_HYPOTHESIS**

---

## 1. O Conceito de Bootstrap Estrutural
Quando uma ideia recém-chegada entra no sistema no estado `RAW_IDEA`, seu genoma é necessariamente esparso. Isso não é uma falha ou defeito; é um regime cognitivo natural denominado **`STRUCTURE_BOOTSTRAP`**.

Durante o bootstrap, a ideia ainda não possui definições suficientemente claras para que o sistema possa avaliar a relevância decisória de incertezas sofisticadas. O objetivo exclusivo deste regime é **obter legibilidade estrutural mínima** (`StructureGain`).

---

## 2. Métricas de Progresso: O que Conta vs O que Não Conta

### ✅ O que Conta como StructureGain Real:
- Identificação de uma nova claim atômica e falsificável.
- Mapeamento de relações explícitas entre claims (`depends_on`, `contradicts`, etc.).
- Exposição de uma premissa implícita (`Assumption`) oculta.
- Identificação do frame dominante de interpretação (`Frame`).
- Separação clara entre a formulação do problema e a proposta de solução.
- Identificação de uma decisão ou bifurcação futura necessária.
- Formulação de um primeiro teste ou verificação empírica concebível.
- Criação de uma alternativa ou contra-hipótese viável.

### ❌ O que NÃO Conta como Progresso:
- Aumento do volume de texto ou reformulação prolixa da ideia.
- Paráfrases, resumos executivos ou embelezamento retórico.
- Criação de claims duplicadas ou sinônimas.
- Múltiplos modelos concordando com a mesma descrição genérica.

---

## 3. Saturação Estrutural (Structure Saturation)
O regime de bootstrap não pode ser infinito. Se após sucessivas rodadas de estruturação o sistema produzir apenas paráfrases, relações redundantes e nenhuma nova claim material ou incerteza exposta, a política de saturação é acionada:
- O sistema registra saturação e obriga o encerramento do bootstrap ou a transição para `REPLAN_REQUIRED`.
- O orçamento de compute (*token budget*) limita o custo máximo sem alterar a avaliação de verdade.
