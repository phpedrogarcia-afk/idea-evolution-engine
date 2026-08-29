# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-01-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um aplicativo de cronômetro pomodoro minimalista para desktop que bloqueia notificações de outros apps durante os blocos de foco de 25 minutos.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um aplicativo desktop minimalista que funcione como cronômetro pomodoro de 25 minutos e silencie as notificações de outros apps durante o período de foco.
- **Problema Central:** Usuários precisam de uma forma de manter foco durante sessões de trabalho de 25 minutos, evitando interrupções de notificações de outros aplicativos.
- **Atores / Usuários:** Usuários de desktop, Profissionais que utilizam a técnica Pomodoro, Estudantes que buscam foco


## 3. Versão Refinada e Mecanismo Proposto

Aplicativo desktop minimalista que funciona como cronômetro pomodoro de 25 min e silencia notificações de outros apps durante o foco usando o modo nativo "Não Perturbe" com lista de exceções para alertas críticos.


- **Justificativa de Promoção ao Core:** Esta abordagem atende diretamente à intenção do usuário de silenciar notificações de forma confiável, utiliza recursos já existentes nos sistemas operacionais e requer apenas permissão do usuário, reduzindo complexidade e necessidade de serviços em segundo plano. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** O aplicativo pode não conseguir bloquear notificações em todos os sistemas operacionais ou versões devido a restrições de API ou permissões elevadas
   - *Impacto:* Se as notificações não forem silenciadas, o objetivo principal de melhorar o foco falha, tornando o aplicativo inútil para muitos usuários
   - *Parte Afetada:* Módulo de bloqueio de notificações
2. **[HIGH]** Bloquear notificações pode impedir alertas críticos (ex.: chamadas de emergência, alarmes do sistema)
   - *Impacto:* Interferir em notificações essenciais pode causar riscos de segurança ou perda de informações importantes, gerando desconfiança no usuário
   - *Parte Afetada:* Gerenciamento de permissões de notificação


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Ativar o modo "Não Perturbe" (Do Not Disturb) nativo do sistema operacional, configurando uma lista de exceções para alertas críticos (chamadas de emergência, alarmes do sistema) e restaurando o estado ao final do pomodoro
   - *Tradeoffs:* Depende da disponibilidade e consistência da API Do Not Disturb em cada SO (Windows, macOS, Linux), Requer permissão de usuário para alterar o estado do sistema, Alguns aplicativos podem ignorar o modo DND, deixando notificações passar
2. **Mecanismo:** Sobrepor a tela com um "focus overlay" que silencia o áudio do sistema e intercepta janelas de notificação, descartando-as exceto as que correspondam a uma lista de aplicativos críticos configurada pelo usuário
   - *Tradeoffs:* Requer automação de UI que pode ser frágil a atualizações de aplicativos ou do SO, Pode causar atraso visual ao fechar notificações, Não impede notificações que não geram janela (ex.: sons de sistema)
3. **Mecanismo:** Daemon leve multiplataforma que, durante o intervalo de foco, usa as APIs de notificação de cada SO (Toast no Windows, Notification Center no macOS, D-Bus no Linux) para silenciar temporariamente todas as aplicações, exceto aquelas marcadas como críticas em uma whitelist configurável
   - *Tradeoffs:* Necessita implementação separada para cada plataforma, aumentando a complexidade de desenvolvimento, Exige permissões elevadas ou instalação de serviço em segundo plano, Manutenção contínua para acompanhar mudanças nas APIs de notificação


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Sobrepor a tela com um "focus overlay" que silencia áudio e descarta notificações exceto as críticas
2. *[CANDIDATE]* Daemon leve multiplataforma que usa APIs de notificação de cada SO para silenciar temporariamente todas as aplicações, exceto as whitelist


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Overlay de foco que intercepta janelas de notificação (Origem: ALTERNATIVES)
  *Motivo:* Pode ser frágil frente a atualizações de UI e não cobre notificações sem janela, aumentando risco de perda de alertas


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Ativar o modo "Não Perturbe" (Do Not Disturb) nativo do sistema operacional, configurando exceções para alertas críticos e restaurando o estado ao final do pomodoro.)

**Dependências Externas do Core:**
- Acesso programático ao modo "Não Perturbe" em Windows (ex.: registro ou PowerShell), macOS (AppleScript/NSUserNotificationCenter) e Linux (dconf ou dbus para GNOME/KDE)
- Permissões de usuário para modificar configurações de notificação em cada SO
- Capacidade de definir listas de exceção/whitelist via API nativa ou contornar limitações com regras de prioridade
- Mecanismo confiável para ler e restaurar o estado pré‑existente do modo Não Perturbe
- Bibliotecas ou bindings que permitam interagir com as APIs de notificação de cada plataforma

**Testes Discriminativos do Core:**
- [ ] Teste unitário que chama a API de DND no Windows 10/11 e verifica se o estado muda para "On" e volta para "Off" após 5 s
- [ ] Teste de script AppleScript no macOS Big Sur que habilita o modo "Não Perturbe", envia uma notificação de teste e confirma que ela é suprimida
- [ ] Teste em Ubuntu GNOME que usa dconf para ativar "Do Not Disturb", envia uma notificação via notify‑send e verifica a ausência de exibição
- [ ] Teste de criação de whitelist no macOS (ex.: permitir notificações de "Calendário") e validar que notificações desse app ainda aparecem enquanto DND está ativo
- [ ] Teste de restauração automática: salvar estado atual, ativar DND, aguardar 1 min, desativar e comparar estado final com o salvo


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementação de "focus overlay" que cobre a tela e silencia áudio do sistema; medir impacto na usabilidade
- [ ] *[EXPLORATÓRIO]* Daemon multiplataforma que intercepta chamadas de notificação via APIs específicas (Toast, Notification Center, D‑Bus) e aplica filtro de whitelist
- [ ] *[EXPLORATÓRIO]* Uso de biblioteca de terceiros (ex.: electron-notification-state) para abstrair controle DND e comparar cobertura de plataformas
- [ ] *[EXPLORATÓRIO]* Teste de integração com gerenciadores de energia para pausar o timer quando o laptop entra em modo de suspensão


## 10. Próximo Passo Recomendado

Implementar um protótipo que ativa o modo Do Not Disturb nas principais plataformas (Windows, macOS, Linux), incluir configuração de exceções críticas e validar o comportamento em cenários de permissão e restauração automática.
