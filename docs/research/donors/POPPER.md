# POPPER — Popperian Sequential Falsification (Berkeley/Oxford)

> **AUTÓPSIA DE DOADOR — STATUS: ADAPT (Level B)**

---

## 1. O que é o Doador
O sistema **POPPER** implementa falsificação sequencial automatizada, traduzindo hipóteses científicas em implicações observáveis e desenhando experimentos discriminativos com garantias estatísticas (e-values).

---

## 2. Mecanismos Analisados
1. **Tradução Hipótese $\to$ Implicação Mensurável:** Separação estrita entre a teoria abstrata e o que precisa ser observado no mundo se ela for verdadeira ou falsa.
2. **Desenho de Experimento vs Execução:** O protocolo desenha o teste antes de autorizar a coleta de evidências.
3. **Falsificação Sequencial:** Priorização de testes capazes de derrubar a hipótese com o menor custo de amostragem.

---

## 3. Riscos e Fraquezas Reveladas no Doador
- **Hiperfoco em Métricas Estatísticas:** O uso irrestrito de *e-values* e inferência sequencial não se aplica a claims qualitativas, de modelo de negócio ou éticas.

---

## 4. Decisão de Transplante para o IEE
- **Adotado:** A disciplina de decomposição da claim em implicações mensuráveis no `TestContract` e a transição para `READY_TO_TEST`.
- **Rejeitado:** Universalização de *e-values* para todas as classes de evidência (suporte a múltiplos `verification_modes`).
