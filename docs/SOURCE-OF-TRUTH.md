# SOURCE-OF-TRUTH.md — Hierarquia Formal de Autoridade Documental

> Este documento define a precedência irrestrita de autoridade de todas as fontes de verdade dentro do projeto **Idea Evolution Engine (IEE)**.

---

## 1. Hierarquia Estrita de Precedência
Em caso de conflito, ambiguidade ou contradição entre quaisquer dois documentos ou declarações, a precedência deve seguir rigorosamente a ordem abaixo (do nível mais alto para o mais baixo):

```text
NÍVEL 1: GOVERNANCE-INVARIANTS.md
   ↓ (Prevalece sobre tudo)
NÍVEL 2: DECISIONS-LEDGER.md
   ↓ (Decisões arquiteturais registradas)
NÍVEL 3: CURRENT-STATE.md
   ↓ (O que existe de fato fisicamente)
NÍVEL 4: SPECS E POLÍTICAS VERSIONADAS (docs/specs/)
   ↓ (Contratos e regras canônicas de transição)
NÍVEL 5: SCHEMAS E TESTES DETERMINÍSTICOS (quando existirem)
   ↓ (Código de validação de baixo nível)
NÍVEL 6: DOCUMENTOS DE ARQUITETURA ALVO (docs/architecture/)
   ↓ (Modelos e especificações para fases futuras)
NÍVEL 7: PESQUISA E AUTÓPSIAS DE DOADORES (docs/research/)
   ↓ (Hipóteses e análises de terceiros)
NÍVEL 8: NOTAS HISTÓRICAS E CONVERSAS ANTERIORES
     (Não possuem autoridade normativa ou técnica)
```

---

## 2. Regras de Interpretação e Resolução de Conflitos

### 2.1 Research não vira Arquitetura Silenciosamente
Um paper, análise de doador ou hipótese descrita em `docs/research/` é estritamente uma fonte de inspiração investigativa (`RESEARCH` / `CANDIDATE`). Nenhuma IA ou desenvolvedor pode tratá-la como componente do sistema sem um registro formal de decisão aprovado em [`DECISIONS-LEDGER.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/DECISIONS-LEDGER.md) e especificação em `docs/specs/`.

### 2.2 TARGET não é CURRENT
Documentos em `docs/architecture/` descrevem o desenho pretendido do sistema completo. Eles NÃO indicam que os módulos estão codificados, operacionais ou disponíveis. A única referência sobre o que está ativo e implementado é [`CURRENT-STATE.md`](file:///c:/Users/phped/Documents/ProjetoFioIedeias/docs/CURRENT-STATE.md).

### 2.3 Conversa e Memória não têm Autoridade
Nenhum contexto discutido em sessões passadas de chat, e nenhuma declaração em chats de IA possui autoridade sobre o código ou a documentação. Se uma ideia não estiver escrita e versionada nos documentos canônicos do repositório, ela formalmente **não existe**.

### 2.4 Reversibilidade e Imutabilidade
- Nenhuma decisão antiga no `DECISIONS-LEDGER.md` pode ser apagada. Se uma decisão for superada, ela é marcada como `SUPERSEDED` com link para a nova decisão e a justificativa empírica da revisão.
- Documentos de especificação congelados (`v0.1`, etc.) são imutáveis; alterações requerem incremento de versão (`v0.2`).
