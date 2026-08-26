# ARBITEROS — Instruction Binding & Dual Validation

> **AUTÓPSIA DE DOADOR — STATUS: ADOPT-CONCEPT (Level C)**

---

## 1. O que é o Doador
O **ArbiterOS** propõe um sistema operacional seguro para agentes LLM, separando o plano semântico (geração probabilística de intenção) do plano de execução determinístico (validação de comandos e checagem de autoridade).

---

## 2. Mecanismos Analisados
1. **Formal Instruction Binding:** Vinculação estrita entre o comando emitido pelo agente e um contrato de execução validável.
2. **Dual Validation (Static + Runtime):** Validação estática de schema/tipos combinada com validação dinâmica de integridade e permissões de segurança.
3. **Structured Data over Executable Code:** Proibição de código executável arbitrário gerado por IA; adoção exclusiva de payloads de dados tipados.

---

## 3. Riscos e Fraquezas Reveladas no Doador
- **Overhead de Validação em Runtime:** Complexidade potencial de validação se as regras não forem puramente determinísticas.

---

## 4. Decisão de Transplante para o IEE
- **Adotado:** A arquitetura do `GenomeValidator` com 5 camadas determinísticas e a regra de que LLMs geram apenas dados tipados (`GenomePatch`), nunca comandos diretos de mutação.
