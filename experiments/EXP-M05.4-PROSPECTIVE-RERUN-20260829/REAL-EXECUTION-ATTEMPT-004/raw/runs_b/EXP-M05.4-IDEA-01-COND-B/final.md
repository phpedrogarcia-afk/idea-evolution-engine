# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-01-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um aplicativo de cronômetro pomodoro minimalista para desktop que bloqueia notificações de outros apps durante os blocos de foco de 25 minutos.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um aplicativo desktop minimalista que funcione como cronômetro Pomodoro de 25 minutos e bloqueie as notificações de outros apps enquanto o usuário está focado.
- **Problema Central:** Usuários são interrompidos por notificações de outros aplicativos durante períodos de foco de 25 minutos, dificultando a concentração.
- **Atores / Usuários:** Usuários de desktop, Profissionais que utilizam a técnica Pomodoro, Estudantes, Trabalhadores remotos


## 3. Versão Refinada e Mecanismo Proposto

Aplicativo desktop minimalista que funciona como cronômetro Pomodoro de 25 minutos e silencia as notificações de outros aplicativos durante o período de foco, usando recursos nativos do sistema para bloquear interrupções.


- **Justificativa de Promoção ao Core:** O modo DND já existe nos principais sistemas operacionais, oferece bloqueio de notificações de forma confiável e requer pouca intervenção adicional, alinhando‑se ao objetivo de um aplicativo minimalista e ao desejo explícito do usuário de silenciar interrupções. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** OS-level notification blocking may be unsupported or restricted on major platforms (e.g., macOS, iOS)
   - *Impacto:* If the app cannot silence notifications, its core value proposition fails, rendering the product ineffective.
   - *Parte Afetada:* Notification blocking module
2. **[MEDIUM]** Indiscriminate blocking can suppress critical or emergency notifications
   - *Impacto:* Users may miss important alerts (security, health, system warnings), leading to potential harm and loss of trust.
   - *Parte Afetada:* Notification filtering logic
3. **[MEDIUM]** Fixed 25‑minute interval with no customization limits usability for users with different work rhythms
   - *Impacto:* Lack of flexibility can cause users to abandon the app, reducing adoption and market fit.
   - *Parte Afetada:* Timer settings UI


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Ativar o modo "Do Not Disturb" (DND) do sistema via API, permitindo ao usuário definir uma lista de exceção para notificações críticas e oferecendo ajuste de duração do Pomodoro na própria UI
   - *Tradeoffs:* Depende do suporte nativo ao DND em cada SO, podendo falhar em versões mais antigas, Requer permissão do usuário para alterar o estado do DND, Não bloqueia notificações que ignoram o DND, como alertas de segurança
2. **Mecanismo:** Criar uma sobreposição transparente em tela cheia que captura eventos de notificação via hooking de APIs específicas, silenciando-as durante o intervalo e permitindo ao usuário escolher qualquer duração para o Pomodoro
   - *Tradeoffs:* Necessita de privilégios elevados ou permissões de acessibilidade, o que pode assustar usuários, Implementação altamente dependente do SO, aumentando a complexidade de manutenção, A sobreposição pode interferir em fluxos de trabalho que exigem acesso rápido ao desktop
3. **Mecanismo:** Executar um serviço de fundo que silencia o áudio do sistema e desativa temporariamente a conectividade de rede para aplicativos não essenciais durante a sessão Pomodoro, com timer configurável via UI mínima
   - *Tradeoffs:* Pode interromper processos legítimos que dependem de áudio ou rede, como chamadas de voz ou atualizações importantes, Requer que o usuário classifique aplicativos como essenciais ou não, aumentando a carga de configuração, A eficácia varia conforme o controle que o SO oferece sobre áudio e rede


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Criar uma sobreposição transparente em tela cheia que captura eventos de notificação via hooking de APIs específicas, silenciando-as durante o intervalo
2. *[CANDIDATE]* Executar um serviço de fundo que silencia o áudio do sistema e desativa temporariamente a conectividade de rede para aplicativos não essenciais durante a sessão Pomodoro


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Sobreposição transparente em tela cheia que captura eventos de notificação (Origem: ALTERNATIVES)
  *Motivo:* Requer privilégios elevados ou permissões de acessibilidade, aumenta complexidade e pode interferir no fluxo de trabalho do usuário
- **Rejeitado:** Serviço de fundo que silencia áudio e desativa rede (Origem: ALTERNATIVES)
  *Motivo:* Pode interromper processos legítimos (ex.: chamadas de voz), exige classificação manual de aplicativos e depende de controles de SO limitados


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Usar a API nativa do sistema para ativar o modo "Do Not Disturb" (DND) durante o intervalo Pomodoro, permitindo ao usuário definir exceções para notificações críticas e ajustar a duração do timer via UI mínima.)

**Dependências Externas do Core:**
- Acesso à API nativa de DND do sistema operacional (ex.: Windows Focus Assist, macOS Notification Center, Linux Dunst ou equivalente).
- Permissões de usuário para modificar configurações de DND.
- Biblioteca/framework GUI compatível com o SO alvo (ex.: Electron, Qt, Tkinter).
- Capacidade de persistir configurações de exceção entre sessões.

**Testes Discriminativos do Core:**
- [ ] Teste de ativação do DND via API ao iniciar o timer e verificação visual de que o modo está ativo.
- [ ] Teste de desativação automática do DND ao término do intervalo Pomodoro.
- [ ] Teste de adição e remoção de exceções de notificação e confirmação de que notificações críticas ainda são entregues.
- [ ] Teste de persistência das configurações de exceção após reinício da aplicação.
- [ ] Teste de UI: ajuste de duração do timer reflete corretamente no comportamento do DND.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementar sobreposição transparente em tela cheia que captura eventos de notificação via hooking e medir eficácia de silenciamento.
- [ ] *[EXPLORATÓRIO]* Desenvolver serviço de fundo que silencia áudio do sistema durante o Pomodoro e avaliar impacto na experiência do usuário.
- [ ] *[EXPLORATÓRIO]* Desativar temporariamente a conectividade de rede para aplicativos não essenciais e medir se isso reduz interrupções.
- [ ] *[EXPLORATÓRIO]* Avaliar uso de APIs de controle de energia para colocar o monitor em modo de baixa energia durante o foco.
- [ ] *[EXPLORATÓRIO]* Testar integração com ferramentas de gerenciamento de tarefas para iniciar automaticamente o timer Pomodoro.


## 10. Próximo Passo Recomendado

Desenvolver um protótipo que ative o modo Do Not Disturb via API nativa, inclua interface mínima para definir exceções e ajustar a duração, e testar o comportamento em macOS, Windows e Linux para validar a eficácia e identificar ajustes necessários.
