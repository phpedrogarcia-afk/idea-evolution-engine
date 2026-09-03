# Pacote Lean de Maturação — Run EXP-M05.5R2-H04-COND-C

**Status:** `HUMAN_DECISION_REQUIRED` | **Chamadas de Modelo Utilizadas:** 1 (Max: 2)

---

## 1. Fonte Humana Imutável (SourceAnchor)

> Quero organizar meus registros pessoais de saúde e sintomas para perceber padrões antes das consultas, mas não quero enviar esses dados para aplicativos, contas online ou serviços de terceiros. Preciso conseguir usar isso no meu próprio computador.


## 2. Intenção & Problema Estruturado (Lean First Pass)

- **Intenção do Usuário:** Criar uma ferramenta que permita ao usuário registrar, armazenar e analisar seus próprios dados de saúde no computador pessoal, garantindo privacidade total.
- **Problema Interpretado:** Organizar registros pessoais de saúde e sintomas localmente para perceber padrões antes das consultas, sem depender de serviços online ou terceiros.

## 3. Mecanismo Primário Proposto

**Mecanismo:** Aplicativo desktop local com interface de entrada de dados e visualização de tendências (gráficos, tabelas) usando análises simples como médias móveis e detecção de correlações.
- **Base de Autoridade Auditada:** `MODEL_HYPOTHESIS`
- **Justificativa:** Um software instalado localmente evita a necessidade de enviar dados a servidores externos, atendendo ao requisito de privacidade enquanto fornece recursos de análise.


## 4. Alternativas Concorrentes Identificadas

1. **Planilha Excel ou CSV com macros ou scripts Python para análise de dados.** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Interface menos amigável para usuários não técnicos, Gerenciamento manual de versões pode levar a inconsistências, Segurança depende das permissões do arquivo local
2. **Software de diário de saúde offline (ex.: OpenMRS local, Joplin com plugins).** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Possível excesso de funcionalidades desnecessárias, Customização limitada para análise de padrões específicos, Dependência de manutenção da comunidade do software
3. **Ferramenta de visualização de dados local (ex.: PowerBI Desktop ou Tableau Public offline).** (Base: `MODEL_HYPOTHESIS`)
   - *Tradeoffs:* Licenças podem ser caras ou restritas, Requer preparação dos dados em formatos específicos, Não oferece captura de dados, apenas visualização


## 5. Avaliação do Early Epistemic Gate (Custo = 0 chamadas)

- **Veredito do Gate:** `REQUEST_HUMAN_DECISION`
- **Motivo de Escalação:** `NONE`
- **Explicação:** A transição exige escolha normativa/humana protegida. Mais raciocínio de IA não substitui autoridade humana.
- **Autoridade Usurpada Detectada:** `False`
- **Candidatos Não Ancorados:** 4

## 7. Próximo Passo Recomendado

Desenvolver um protótipo mínimo viável (MVP) de aplicativo desktop que permita entrada de dados de saúde, armazenamento criptografado localmente e geração de gráficos simples; testar com um pequeno grupo de usuários para validar usabilidade e identificar necessidades de backup seguro.
