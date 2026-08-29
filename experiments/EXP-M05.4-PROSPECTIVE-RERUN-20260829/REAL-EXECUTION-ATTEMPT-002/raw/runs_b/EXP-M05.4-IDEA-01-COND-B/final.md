# Pacote de Maturação da Ideia — Run EXP-M05.4-IDEA-01-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Um aplicativo de cronômetro pomodoro minimalista para desktop que bloqueia notificações de outros apps durante os blocos de foco de 25 minutos.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um aplicativo de cronômetro pomodoro minimalista para desktop que bloqueie as notificações de outros apps durante os blocos de foco de 25 minutos.
- **Problema Central:** Usuários têm dificuldade de manter foco porque notificações de outros aplicativos interrompem sessões de trabalho de 25 minutos.
- **Atores / Usuários:** Profissionais que trabalham em desktop, Estudantes que estudam no computador, Freelancers que precisam de sessões de foco


## 3. Versão Refinada e Mecanismo Proposto

Aplicativo desktop minimalista de pomodoro de 25 minutos que, ao iniciar, ativa o modo Não Perturbe do sistema e permite ao usuário definir uma lista branca de alertas críticos, com opção de escolher a duração da sessão.


- **Justificativa de Promoção ao Core:** Garante foco bloqueando distrações enquanto preserva alertas essenciais, atendendo diretamente à intenção humana de bloqueio de notificações durante blocos de foco. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Dependência de controle de notificações que nem todos os sistemas operacionais suportam
   - *Impacto:* Se o SO não permite que apps de terceiros bloqueiem notificações, a funcionalidade central falha, tornando o produto inútil
   - *Parte Afetada:* Mecanismo de bloqueio de notificações
2. **[HIGH]** Bloqueio indiscriminado pode impedir alertas críticos (ex.: chamadas de emergência, alarmes)
   - *Impacto:* Perder notificações importantes pode colocar a segurança do usuário em risco e gerar rejeição ao app
   - *Parte Afetada:* Política de bloqueio de notificações
3. **[MEDIUM]** Suposição de que todos os usuários preferem sessões fixas de 25 minutos
   - *Impacto:* Usuários com necessidades diferentes (ex.: tarefas curtas ou longas) podem achar o app inflexível e abandoná‑lo
   - *Parte Afetada:* Configuração de tempo padrão


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implementar um serviço de filtragem de notificações cross‑platform (ex.: usando Electron + node‑notifier) que, ao iniciar o pomodoro, intercepta as notificações do sistema e silencia apenas as que não estão na lista branca configurada pelo usuário. Quando o modo Não Perturbe nativo não está disponível, o serviço age como fallback.
   - *Tradeoffs:* Necessita permissões elevadas ou instalação de um serviço em segundo plano, o que pode ser complexo para usuários menos técnicos, A camada de filtragem pode introduzir latência na entrega de notificações legítimas
2. **Mecanismo:** Criar um "modo foco interno" que, ao iniciar o timer, escurece a tela, pausa sons de aplicativos e exibe um overlay; ao mesmo tempo, um módulo de detecção de emergência (ex.: análise de áudio para sons de alarme ou chamada) reativa temporariamente as notificações críticas quando detectado.
   - *Tradeoffs:* Detecção de áudio pode gerar falsos positivos/negativos e consome recursos de CPU, Requer acesso ao microfone, o que pode levantar preocupações de privacidade
3. **Mecanismo:** Oferecer o timer como aplicação web leve que usa apenas notificações do navegador e, opcionalmente, um pequeno helper nativo que bloqueia notificações de aplicativos específicos (não todo o sistema). O usuário pode escolher a duração da sessão (25 min, 30 min, etc.) e definir quais apps podem notificar durante o foco.
   - *Tradeoffs:* O helper nativo precisa ser instalado separadamente, aumentando a barreira de adoção, Bloqueio por aplicativo pode não cobrir todas as fontes de interrupção (ex.: mensagens de sistema)


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Implementar um serviço de filtragem de notificações cross‑platform que silencia notificações não listadas na whitelist quando o modo Não Perturbe nativo não está disponível
2. *[CANDIDATE]* Criar um "modo foco interno" com overlay escuro e detecção de áudio para reativar notificações críticas
3. *[CANDIDATE]* Oferecer o timer como aplicação web leve com helper nativo opcional para bloqueio de notificações por aplicativo


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Serviço de filtragem de notificações cross‑platform que requer permissões elevadas (Origem: ALTERNATIVES)
  *Motivo:* Complexidade de instalação e risco de segurança para usuários menos técnicos
- **Rejeitado:** Modo foco interno com detecção de áudio para emergências (Origem: ALTERNATIVES)
  *Motivo:* Consome recursos de CPU, pode gerar falsos positivos/negativos e levanta preocupações de privacidade


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Ativar o modo Não Perturbe do sistema ao iniciar o pomodoro e permitir ao usuário definir uma lista branca de notificações críticas.)

**Dependências Externas do Core:**
- API nativa de controle do modo Não Perturbe disponível e documentada para cada SO alvo (Windows, macOS, Linux).
- Permissão do usuário concedida para alterar o estado de DND (ex.: via prompt de segurança ou configuração de política).
- Acesso ao gerenciador de notificações para identificar e permitir exceções da lista branca.
- Persistência de configurações de whitelist entre sessões (arquivo de configuração ou armazenamento seguro).
- Capacidade de restaurar o estado original de DND ao término do pomodoro.

**Testes Discriminativos do Core:**
- [ ] Teste de ativação do modo Não Perturbe ao iniciar o pomodoro em Windows 10/11 e verificação de estado via API.
- [ ] Teste de ativação do modo Não Perturbe em macOS 13+ e confirmação visual/por API.
- [ ] Teste de ativação do modo Não Perturbe em Ubuntu GNOME 22.04 e verificação de estado.
- [ ] Teste de entrega de notificações incluídas na whitelist enquanto DND está ativo em cada SO.
- [ ] Teste de bloqueio de notificações não listadas na whitelist enquanto DND está ativo.
- [ ] Teste de restauração automática do estado original de DND ao término do timer.
- [ ] Teste de persistência da lista branca entre reinicializações do aplicativo.


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Implementar e testar um serviço cross‑platform de filtragem de notificações (ex.: Electron + node‑notifier) que silencia notificações fora da whitelist quando DND nativo não está disponível.
- [ ] *[EXPLORATÓRIO]* Desenvolver um modo foco interno com overlay escuro, pausa de áudio e detecção de sons críticos para reativar notificações críticas, e validar a precisão da detecção de áudio.
- [ ] *[EXPLORATÓRIO]* Criar uma versão web leve do timer que usa a API de Notificações do navegador e um helper nativo opcional para bloquear notificações de aplicativos específicos, testando a integração entre web e helper.


## 10. Próximo Passo Recomendado

Desenvolver um protótipo que alterna o modo Não Perturbe do sistema e gerencia a whitelist, testá‑lo nos principais sistemas operacionais (Windows, macOS, Linux) e coletar feedback de usuários sobre a personalização da duração da sessão.
