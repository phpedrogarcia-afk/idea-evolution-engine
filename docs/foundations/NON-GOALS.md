# NON-GOALS.md — Antiobjetivos e Limites Estritos de Escopo

> Este documento define explicitamente o que o **Idea Evolution Engine (IEE)** **NÃO É** e o que o projeto **NÃO SE PROPÕE A FAZER**.

---

## 1. Antiobjetivos Estruturais e de Produto

### ❌ 1. Não é um Chat Multiagente Informal
O IEE não é uma sala de bate-papo onde diferentes personas de IA conversam livremente em linguagem natural. Toda interação deve ocorrer sob um contrato tipado (`DeliberationContract`) gerando propostas estruturadas (`GenomePatch`).

### ❌ 2. Não é um Conselho de IAs Votando
O IEE não utiliza votação majoritária ou média ponderada de opiniões de LLMs para decidir se uma ideia é válida. Decisões requerem evidência verificável ou autoridade humana soberana.

### ❌ 3. Não é uma Fábrica Automática de Startups / Pitch Generator
O sistema não busca produzir resumos executivos superficiais, slogans de marketing ou apresentações de vendas automáticas. O foco é a integridade epistêmica, a falsificabilidade e a viabilidade técnica/empírica da ideia.

### ❌ 4. Não é uma Máquina que Decide se uma Ideia é "Boa" ou "Ruim"
O IEE não atribui notas morais ou estéticas abstratas. Ele mapeia: *o que precisa ser verdade, o que já é suportado por evidência, quais premissas continuam incertas e qual teste deve ser executado*.

### ❌ 5. Não é um Substituto do Criador Humano
A IA atua como assistente de investigação, crítica adversarial e sintetizadora; ela não detém soberania sobre a intenção, os valores centrais ou a decisão de avançar, pivotar ou descartar a ideia.

### ❌ 6. Não é um Módulo Interno do FioOS
O IEE é uma aplicação cognitiva de governança de ideias totalmente autônoma. Ele não depende internamente do kernel do FioOS para sua lógica epistêmica e pode ser executado sobre executores locais determinísticos.

### ❌ 7. Não é uma Teoria Universal e Fechada da Criatividade
O IEE não reivindica ter descoberto a fórmula matemática definitiva da inovação humana. Ele implementa um protocolo pragmático e rigoroso de redução de incerteza e falsificação sequencial.

### ❌ 8. Não é um Gerador de Texto Extenso
A qualidade do sistema não é medida pelo volume de tokens gerados. Respostas prolixas que não alteram a estrutura do genoma são consideradas estagnação (*No Measurable Progress*).

---

## 2. A Ilusão do Pipeline Ingênuo
Uma implementação que simplesmente realize:
```text
IA A (Gera) → IA B (Critica) → IA C (Sintetiza) → Summary Final
```
**NÃO satisfaz a visão e a constituição do Idea Evolution Engine.** O IEE exige memória durável imutável (`IdeaGenome`), validação de integridade determinística, gestão de tensões e contratos prévios de deliberação.
