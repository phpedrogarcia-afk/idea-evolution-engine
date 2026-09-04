# FioIdeias V1 — Lean L1 Default

> **Sistema de Maturação e Investigação Deliberativa de Ideias com Preservação Estrita de Intenção e Soberania Humana.**

---

## 🎯 O que é o FioIdeias?

O **FioIdeias** recebe uma ideia crua e a retorna significativamente mais clara, criticada, contextualizada e refinada através de um processo de IA controlado e auditável, preservando a intenção humana original e distinguindo categoricamente o que veio do usuário do que foi inferido ou proposto pelo sistema.

### O que o FioIdeias NÃO é:
- ❌ **Não é um gerador autônomo de verdade:** Ele não inventa fatos nem decide o que é empiricamente verdadeiro no mundo real sem testes.
- ❌ **Não é um designer autônomo de produtos:** Ele não toma decisões executivas ou de implementação pelo usuário.
- ❌ **Não é uma garantia de ideia correta:** Ele mapeia riscos, alternativas e incertezas cruciais para que o humano tome decisões melhores.

---

## ⚡ Instalação e Requisitos

### Pré-requisitos
- Python 3.10 ou superior
- Chave de API de provedor gratuito suportado (atualmente **Cerebras Free Tier**)

### Instalação Canônica
```bash
# Clone o repositório
git clone https://github.com/phpedrogarcia-afk/idea-evolution-engine.git
cd idea-evolution-engine

# Instale o pacote em modo editável ou padrão
pip install -e .
```

### Execução Direta Sem Instalação
O repositório também inclui executores nativos convenientes para desenvolvimento:
- **Windows (PowerShell / CMD):** `.\iee.cmd evolve "<sua ideia>"`
- **Linux / macOS (Bash):** `./iee evolve "<sua ideia>"`
- **Módulo Python direto:** `python -m src.idea_evolution.cli.main evolve "<sua ideia>"`

---

## 🔑 Configuração de Provedor & Política de Custo Zero

O FioIdeias opera sob uma **política estrita de custo de bolso zero** (`OUT_OF_POCKET_COST = ZERO`, `PAID_INFERENCE_ALLOWED = NO`):

```bash
# Configure a chave gratuita da Cerebras
export CEREBRAS_API_KEY="sua_chave_aqui"       # Linux/macOS
$env:CEREBRAS_API_KEY="sua_chave_aqui"        # Windows PowerShell
```

> [!NOTE]
> **Ressalva de Transparência Epistêmica sobre Custos:**  
> O FioIdeias utiliza atualmente a cota gratuita da Cerebras com o modelo `openai/gpt-oss-120b` (transporte `gpt-oss-120b`). A Cerebras é o atual provedor de transporte de inferência livre, e **não** a arquitetura do produto. Não afirmamos que terceiros serão permanentemente gratuitos; termos de uso e cotas de provedores externos podem mudar. Se a elegibilidade gratuita de uma rota não puder ser confirmada em tempo de execução, o FioIdeias **falha de forma fechada (*fail-closed*)** e se recusa a executar, impedindo cobranças financeiras acidentais.

---

## 🚀 Como Usar

### 1. Evolução Padrão de Ideia (Caminho Lean L1)
O caminho padrão do FioIdeias V1 é o **Lean L1 com Early Epistemic Gate**. Ele executa uma primeira passada rigorosa e, caso detecte incerteza material ou vulnerabilidade, despacha no máximo 1 escalação focada (máximo de 2 chamadas de modelo por evolução):

```bash
iee evolve "Um aplicativo simples para organizar empréstimo de ferramentas entre vizinhos"
```

Também é possível carregar uma ideia a partir de um arquivo de texto:
```bash
iee evolve -f minha_ideia.txt
```

### 2. Saída em JSON Estruturado (Contrato de Máquina)
Para integração programática, pipelines ou automações, utilize a flag `--json`. Ela emite o `EvolutionArtifact` (v1.0) canônico serializado:

```bash
iee evolve "Minha ideia" --json
```

### 3. Fallback Rápido de Passada Única (`--fast`)
Se você deseja apenas uma estruturação preliminar sem escalação condicional ou análise profunda de vulnerabilidades:

```bash
iee evolve "Minha ideia" --fast
```

---

## 📋 Estrutura da Apresentação Humana

Ao executar no terminal, o `HumanResultRenderer` formata o resultado em Markdown limpo e auditado com a seguinte estrutura:

1. **Ideia Original:** A transcrição exata da entrada do usuário, sem mutação silenciosa.
2. **Ideia Refinada (Proposta pelo Sistema):** A proposta de formulação clara gerada pelo sistema.
3. **Intenção Identificada:** A leitura da intenção nuclear do usuário, sem usurpação de autoridade.
4. **Pontos de Atenção e Críticas:** Vulnerabilidades técnicas, econômicas ou operacionais detectadas.
5. **Premissas Identificadas:** Suposições não verificadas que sustentam a ideia.
6. **Incertezas Mapeadas:** Lacunas de conhecimento explícitas que exigem validação empírica.
7. **Possibilidades e Alternativas:** Mecanismos concorrentes ou variantes consideradas.
8. **Decisão Humana Necessária:** Apresentada sempre que houver uma bifurcação de valores morais, éticos ou de negócio que a IA não pode e não deve arbitrar sozinha.
9. **Próximo Passo Recomendado:** Ação concreta e falsificável para colocar a ideia à prova no mundo real.

---

## ⚠️ Limitações Conhecidas do V1

1. **Interface de Linha de Comando:** O V1 é focado em terminais (CLI) e geração de artefatos Markdown/JSON. Interfaces gráficas ricas (GUI) e web apps estão planejados para versões futuras.
2. **Contenção Estrita de Chamadas:** O Lean L1 consome no máximo 2 chamadas de modelo por execução para garantir previsibilidade e custo zero.
3. **Pausa para Decisão Humana (`HUMAN_DECISION_REQUIRED`):** Ideias que dependem fundamentalmente de escolhas normativas ou preferências humanas subjetivas não recebem uma resolução automática inventada pela IA; o sistema interrompe o fluxo para que o humano exerça sua soberania deliberativa.
4. **Dependência de Conectividade:** A inferência requer conexão com a internet para comunicação segura com o endpoint gratuito do modelo.

---

## 📚 Documentação Técnica e Arquitetura

Para pesquisadores, desenvolvedores e auditores epistêmicos, a documentação profunda está organizada em [`docs/`](docs/):
- [`docs/INDEX.md`](docs/INDEX.md): Índice mestre de toda a documentação.
- [`docs/m06-productization/`](docs/m06-productization/): Registros formais de transição científica para produto, contratos de arquitetura e portões de aceitação do V1.
- [`docs/GOVERNANCE-INVARIANTS.md`](docs/GOVERNANCE-INVARIANTS.md): Constituição epistêmica e regras invioláveis do repositório.
