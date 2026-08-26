# docs/intelligence/HYPOTHESIS-PROTOCOL.md — Protocolo de Formulação e Ataque de Hipóteses

> **TODA MUTAÇÃO MATERIAL DEVE NASCER COMO UMA HIPÓTESE FALSIFICÁVEL.**
> *Não alterar código ou arquitetura apenas porque "parece melhor".*

---

## 1. Estrutura Canônica de uma Hipótese de Mudança

Toda proposta de alteração estrutural ou intervenção deve declarar:

```markdown
### [HYP-XXX] [Título da Hipótese]
- **Problem:** Qual falha, ineficiência ou gap está sendo atacado?
- **Baseline:** Qual é a medição ou estado atual antes da intervenção?
- **Proposed Change:** Qual é a intervenção mínima proposta?
- **Expected Effect:** Qual ganho mensurável ou estrutural é esperado?
- **Failure Condition:** Sob qual resultado a hipótese será considerada REFUTADA?
- **Measurement / Test:** Como o efeito será mensurado deterministicamente?
```

---

## 2. Regra Fundamental: Diagnóstico Não É Fato
Quando uma IA afirma: *"O problema é a falta de contexto X"* ou *"A causa do bug é a função Y"*, essa declaração é estritamente uma **hipótese diagnóstica**, não um fato estabelecido.
A IA deve produzir evidência reproduzível (ex: teste que falha) antes de aplicar a correção.

---

## 3. Protocolo de Falhas: Transformar Falha em Teste Antes de Memória
> **Importado do FioOS:**
> $\text{FAILURE} \to \text{REPRODUCTION} \to \text{FAILING TEST} \to \text{PATCH} \to \text{PASS} \to \text{REGRESSION TEST} \to \text{PERSISTENCE}$

Nunca resolver uma falha apenas dizendo "lembre-se de não fazer isso". Se uma invariante ou protocolo falhar, deve ser escrito um teste automatizado que impeça a regressão.
