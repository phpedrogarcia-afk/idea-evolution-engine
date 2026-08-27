# FIOED-IDEA-ECOLOGY.md — Ecologia de Ideias, Incubação e Pressão Localizada

> **DOCUMENTO DOUTRINÁRIO E DE ESPECIFICAÇÃO DE DOMÍNIO**
> **STATUS:** `WORKING_RECEIVER_EXTENSION` | `FORMALIZED_OFFLINE` | `CALIBRATION_PENDING`
> **OBJETIVO:** Estabelecer a coexistência constitucional entre Eficiência Epistêmica (não gastar inferência inútil) e Incubação Criativa (não destruir ideias férteis com pressão racional prematura).

---

## 1. Rejeição do Modelo "Apenas Arena"

O FioIdeias rejeita o paradigma reducionista de tratar o pensamento apenas como uma arena competitiva:

$$\text{NÃO:} \quad \text{GERAR} \longrightarrow \text{PONTUAR} \longrightarrow \text{COMPETIR} \longrightarrow \text{SELECIONAR} \longrightarrow \text{MATAR}$$

Em vez disso, adota o modelo de **Ecologia de Ideias**: um ecossistema com múltiplos estados vitais legítimos:
- **Incubação & Dormência:** Ideias ou aspectos preservados sem obrigação de utilidade imediata;
- **Coexistência & Tensão:** Preservação de visões concorrentes sem forçar consenso artificial;
- **Mutação & Simbiose:** Associação de conceitos quando há tensão fértil;
- **Testagem Localizada:** Pressão dirigida estritamente ao mecanismo sob teste ($h_i$), sem invalidar a visão global ($K$);
- **Reentrada sob Novas Condições:** Ideias podadas podem reabrir quando premissas mudam.

---

## 2. Distinções Constitucionais da Ecologia

| Princípio Canônico | O que Afirma | Consequência Operacional no FioED |
| :--- | :--- | :--- |
| **$\text{IdeaWorth} \neq \text{DecisionDelta}$** | O valor existencial/humano de uma ideia não é medido por quão rápido ela gera código. | A ausência de Decision Delta imediato nunca autoriza a exclusão da ideia. |
| **$\text{Unknown} \neq \text{LowValue}$** | Não saber articular um teste não torna a ideia inferior. | Incertezas férteis ($U_f$) são protegidas na Zona de Incubação ($Z_p$). |
| **$\text{NoEvidenceYet} \neq \text{False}$** | A ausência temporária de evidência não é prova de falsidade. | Ideias permanecem no status `CANDIDATE` ou `PRESERVED_UNKNOWN`. |
| **$\text{NotActionableYet} \neq \text{Useless}$** | O que não é acionável hoje pode ser o centro de gravidade amanhã. | Mantido no estado operacional `KEEP`. |
| **$\text{Preservation} \neq \text{Promotion}$** | Proteger uma ideia da morte não significa promovê-la ao Core. | A ideia sobrevive sem invadir o núcleo comprovado do sistema. |
| **$\text{Incubation} \neq \text{Stagnation}$** | Repouso fértil é um processo de maturação não-generativo. | Não exige chamadas cíclicas de LLM para justificar existência. |
| **$\text{FailureOfMechanism} \neq \text{FailureOfVision}$** | A falha de um meio técnico não refuta o objetivo fundamental. | A falha local em $h_i$ rejeita $h_i$, mas preserva o Kernel $K(h)$. |
| **$\text{Comparison} \neq \text{Mandatory}$** | Ideias não precisam ser comparadas só porque coexistem. | Comparação só é permitida se houver disputa real de recursos. |
| **$\text{Consensus} \neq \text{Completion}$** | Eliminar discordâncias empobrece o sistema. | Desacordos são preservados como `TensionRecord`. |
| **$\text{Maturity} \neq \text{Age}$** | O tempo de criação não dita prontidão para pressão. | Prontidão é avaliada pelo vetor `PressureReadiness`. |
| **$\text{CapabilityToTest} \neq \text{ObligationToTest}$** | Ter como testar não obriga a testar agora. | O humano pode emitir `HumanIncubationOverride`. |

---

## 3. As Duas Classes de Incerteza: $U_f$ vs $U_g$

Toda incerteza no FioED é tipada em uma de duas categorias fundamentais:

```text
               ┌───────────────────────────┐
               │    CAMPO DE INCERTEZAS    │
               └─────────────┬─────────────┘
                             │
              ┌──────────────┴──────────────┐
              ▼                             ▼
   ┌───────────────────────┐   ┌───────────────────────┐
   │ U_f: FERTILE UNKNOWN  │   │   U_g: GAP UNKNOWN    │
   │ (Mistério Potencial)  │   │  (Incerteza Formada)  │
   ├───────────────────────┤   ├───────────────────────┤
   │ • Sem pergunta Q*     │   │ • Pergunta clara      │
   │ • Sem interface teste │   │ • Contraste definido  │
   │ • Sem métrica útil    │   │ • Rota de evidência   │
   ├───────────────────────┤   ├───────────────────────┤
   │ AÇÃO: SEE / KEEP      │   │ AÇÃO: PRESS / TEST    │
   │ INCUBAR NA ZONA Z_p   │   │ DISCRIMINAR ESTADO    │
   └───────────────────────┘   └───────────────────────┘
```

### 3.1 Reversibilidade e Falha de Pergunta (Question Failure)
A evolução entre $U_f$ e $U_g$ não é um funil unidirecional irreversível:
$$U_f \xrightarrow{\text{formulação}} \text{EmergentQuestion} \xrightarrow{\text{ligação}} U_g \xrightarrow{\text{teste empírico}} \text{QUESTION\_FAILURE} \xrightarrow{\text{retorno}} U_f$$

- **`HYPOTHESIS_FAILURE`:** A premissa técnica $h_i$ foi falseada pela realidade.
- **`TEST_FAILURE`:** O teste foi mal executado ou ruidoso.
- **`QUESTION_FAILURE`:** A pergunta formulada era míope, capciosa ou não capturava o fenômeno real. O sistema retorna o aspecto para $U_f$ sem descartar a ideia.
- **`INCONCLUSIVE`:** A evidência não permitiu discriminar entre as hipóteses.

---

## 4. Zona de Incubação Protegida ($Z_p$) e Kernel de Identidade ($K$)

### 4.1 Zona de Incubação Protegida ($Z_p$)
Espaço conceitual onde uma ideia é mantida sem exigência de aluguel epistêmico ou Decision Delta imediato.
- **Operações Permitidas:** Observar (`SEE`), Preservar (`KEEP`), Mapear tensões, Propor perguntas emergentes, Associação livre.
- **Operações Proibidas:** Ranking absoluto, pontuação universal, rejeição existencial, promoção automática ao Core.

### 4.2 Kernel de Identidade ($K(h)$)
O núcleo invariante que define a essência da ideia: *O que teria que desaparecer antes que esta deixasse de ser a mesma ideia?*
- **Regra de Autoridade Soberana:** O modelo de IA pode propor `MODEL_INFERRED_KERNEL`, mas apenas a autoridade humana pode confirmar `HUMAN_CONFIRMED_KERNEL`.
- **Isolamento de Falha:** A falha de um mecanismo periférico ($h_{17}$) nunca invalida o Kernel $K(h)$.

---

## 5. Prontidão para Pressão (`PressureReadiness`) e os 4 Verbos

### 5.1 Os 4 Verbos Operacionais
1. **`SEE`:** Observar e registrar o que é, sem obrigação de modificar.
2. **`KEEP`:** Preservar na Zona de Incubação por tempo indeterminado.
3. **`PRESS`:** Aplicar teste ou crítica focalizada sobre um mecanismo específico $h_i$.
4. **`COMMIT`:** Alocar autoridade formal ou adotar decisão definitiva.

### 5.2 Vetor `PressureReadiness` (Sem Score Escalar)
A decisão de aplicar pressão não decorre de uma nota inventada (ex: $0.82$). É um vetor booleano determinístico:
$$\mathbf{PressureReadiness}(h_i) = \langle \text{IdentityRelation}, \text{QuestionFormed}, \text{ContrastDefined}, \text{EvidencePath}, \text{StateDiscrim}, \text{DecisionRelevance}, \text{ScopeContained}, \neg\text{HumanOverride} \rangle$$

---

## 6. Da Pergunta Emergente à Questão Discriminativa ($Q^*$)

```text
FERTILE UNKNOWN (U_f)
        │
        ▼
EMERGENT QUESTION ("O que significa uma memória estar pronta para retornar?")
        │
        ▼
QUESTION CANDIDATE ("A relevância do retorno depende do contexto semântico?")
        │
        ▼
DISCRIMINATING QUESTION Q* (Requer Contraste Observável + Discriminação de Estados)
```

### 6.1 Condição de Discriminação de Estado
Uma pergunta é $Q^*$ SSE existirem pelo menos dois desfechos possíveis legítimos ($o_1, o_2$) que resultem em transições de estado distintas:
$$\text{Transition}(X, o_1) \neq \text{Transition}(X, o_2)$$
Se todos os desfechos possíveis levarem à mesma decisão prática, a pergunta tem valor discriminativo nulo e não deve receber investimento de inferência.

---

## 7. Exemplo Canônico Completo

**Entrada Humana:** *"Um aplicativo que ajuda pessoas a transformar ideias vagas em projetos mais claros."*

1. **Kernel de Identidade Incomutável ($K$):** Ajudar humanos a clarificar pensamentos vagos em projetos executáveis.
2. **Fertile Unknown ($U_f$):** Como representar visualmente a transição de um pensamento caótico sem impor uma estrutura rígida que mate a intuição?
3. **Emergent Question:** Estruturas visuais não-lineares preservam melhor a intuição que formulários?
4. **Mecanismo Candidato ($h_{17}$):** Grafo dinâmico com física de nós que se agrupam por atração semântica local.
5. **Questão Discriminativa ($Q^*$):** *Usuários que utilizam agrupamento semântico por física de nós reportam menor atrito cognitivo que usuários em listas hierárquicas?*
6. **Interface da Realidade Requerida:** `HUMAN_OBSERVATION` / `EXPERIMENT`.
7. **Classe de Evidência Exigida:** `HUMAN_OBSERVATION` (Estudo de usabilidade com sujeitos reais).
8. **Resultado Local de Falha:** Se $h_{17}$ falhar por sobrecarga visual, rejeita-se $h_{17}$ (`REJECT_LOCAL`), mas o Kernel $K$ e o Fertile Unknown $U_f$ permanecem intactos em $Z_p$.
