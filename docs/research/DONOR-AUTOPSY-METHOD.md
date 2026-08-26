# DONOR-AUTOPSY-METHOD.md — Metodologia de Autópsia de Doadores

> **Metodologia de Engenharia Reversa e Transplante Orientado a Gaps**

---

## 1. O Princípio da Adoção Orientada a Gaps
> **Nenhum sistema, paper ou framework entra no IEE sem uma lacuna receptora explícita.**

O projeto proíbe terminantemente o "turismo tecnológico" (adotar ferramentas apenas por estarem em voga). Toda análise de doador externo segue o protocolo rigoroso de autópsia.

---

## 2. O Fluxo Metodológico de Autópsia

```text
┌─────────────────────────────────────────────────────────────┐
│ 1. GAP RECEPTOR NOSSO                                       │
│    Qual problema concreto não sabemos resolver?             │
├─────────────────────────────────────────────────────────────┤
│ 2. SISTEMA DOADOR CANDIDATO                                 │
│    Quem já tentou resolver problema análogo?                │
├─────────────────────────────────────────────────────────────┤
│ 3. MECANISMO REAL                                           │
│    Qual a engrenagem exata (algoritmo, protocolo, schema)?  │
├─────────────────────────────────────────────────────────────┤
│ 4. NÍVEL DE EVIDÊNCIA EMPÍRICA                              │
│    Level A (reproduzido) a Level E (marketing / sem prova)  │
├─────────────────────────────────────────────────────────────┤
│ 5. COMPATIBILIDADE E RISCOS                                 │
│    Viola nossas invariantes? Causa acoplamento ou custo?    │
├─────────────────────────────────────────────────────────────┤
│ 6. HIPÓTESE DE TRANSPLANTE                                  │
│    Como adaptar a engrenagem isoladamente?                  │
├─────────────────────────────────────────────────────────────┤
│ 7. DECISÃO FINAL                                            │
│    KEEP / ADOPT-CONCEPT / ADAPT / DEPEND / REJECT / FUTURE  │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Hierarquia de Evidência dos Doadores
- **LEVEL A:** Peer-reviewed / Benchmark público reproduzido e verificado.
- **LEVEL B:** Preprint confiável com experimentos substantivos e código aberto.
- **LEVEL C:** Arquitetura conceitual / Proof of Concept funcional sem benchmark rigoroso.
- **LEVEL D:** Especulação teórica interessante sem validação empírica.
- **LEVEL E:** Marketing comercial / Alegação de fornecedor sem verificação independente.

---

## 4. Taxonomia de Decisão de Transplante
- `ADOPT-CONCEPT`: Adotar a ideia teórica, reimplementando do zero em nossos termos.
- `ADAPT`: Adaptar a estrutura de dados ou algoritmo para o contexto do IEE.
- `DEPEND`: Adotar como dependência de software externa (excepcional).
- `REJECT`: Incompatível, sem evidência ou violador de invariantes constitucionais.
- `FUTURE_DONOR`: Relevante apenas para fases posteriores (ex: otimização por RL).
