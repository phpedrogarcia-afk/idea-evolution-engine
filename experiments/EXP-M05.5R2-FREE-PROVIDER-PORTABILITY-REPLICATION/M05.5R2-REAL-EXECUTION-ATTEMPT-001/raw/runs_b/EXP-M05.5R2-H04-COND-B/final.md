# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H04-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> Quero organizar meus registros pessoais de saúde e sintomas para perceber padrões antes das consultas, mas não quero enviar esses dados para aplicativos, contas online ou serviços de terceiros. Preciso conseguir usar isso no meu próprio computador.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar uma solução local que permita registrar, organizar e analisar informações de saúde e sintomas, garantindo total privacidade e controle dos dados pelo usuário.
- **Problema Central:** O usuário precisa organizar seus registros pessoais de saúde e sintomas para identificar padrões antes das consultas, mas deseja que esses dados permaneçam exclusivamente no seu próprio computador, sem serem enviados a aplicativos, contas online ou serviços de terceiros.
- **Atores / Usuários:** Usuário que registra os dados, Profissionais de saúde que receberão as informações nas consultas (indireto)


## 3. Versão Refinada e Mecanismo Proposto

Um aplicativo local que permite ao usuário registrar, organizar e visualizar seus dados de saúde e sintomas, armazenando tudo de forma criptografada no dispositivo e realizando backups automáticos para um drive externo criptografado controlado pelo usuário.


- **Justificativa de Promoção ao Core:** Atende diretamente à intenção explícita do usuário de manter os dados totalmente privados e sob seu controle, oferecendo redundância contra perda sem depender de serviços de terceiros. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Data stored only locally is vulnerable to loss, theft, or malware infection
   - *Impacto:* If the health records are compromised or lost, the user loses valuable medical history and may suffer privacy breaches, undermining the core purpose of the system
   - *Parte Afetada:* Data storage and security
2. **[HIGH]** Absence of automatic backup or synchronization increases risk of irreversible data loss
   - *Impacto:* Hardware failures, accidental deletion, or system crashes can erase the entire dataset, leaving the user without any record for future consultations
   - *Parte Afetada:* Data persistence
3. **[MEDIUM]** Assuming the user can manually input and maintain structured health data accurately
   - *Impacto:* Inconsistent or incomplete entries reduce the reliability of pattern analysis, potentially leading to false conclusions or missed health signals
   - *Parte Afetada:* User interaction / data quality
4. **[MEDIUM]** Relying on simple tools for pattern detection may be insufficient for clinically relevant insights
   - *Impacto:* Complex health patterns often require advanced statistical or machine‑learning methods; simplistic visualizations may mislead the user into over‑ or under‑estimating health trends
   - *Parte Afetada:* Analysis engine


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Implementar backup descentralizado via rede P2P (ex.: IPFS ou rede de dispositivos confiáveis) onde os blocos criptografados são replicados em múltiplos nós controlados pelo usuário
   - *Tradeoffs:* Requer configuração inicial de nós confiáveis ou uso de dispositivos adicionais, Dependência de conectividade de rede para sincronização, Aumento do consumo de armazenamento ao replicar dados
2. **Mecanismo:** Incorporar módulos de aprendizado de máquina on‑device que analisam os dados de saúde localmente, permitindo detecção de padrões avançados sem enviar informações para a nuvem
   - *Tradeoffs:* Modelos de ML consomem CPU/GPU e podem exigir atualizações periódicas, Complexidade de desenvolvimento e necessidade de treinamento de modelos com dados limitados
3. **Mecanismo:** Fornecer interface de entrada guiada com validação automática (ex.: formulários estruturados, reconhecimento de voz e integração com dispositivos wearables) para melhorar a precisão e consistência dos registros de saúde
   - *Tradeoffs:* Dependência de hardware adicional (microfone, sensores) ou de APIs de reconhecimento de voz que podem ter limitações offline, Possível curva de aprendizado para usar as novas ferramentas de entrada


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Interface de entrada guiada com formulários estruturados, reconhecimento de voz offline e integração com dispositivos wearables para melhorar a precisão e consistência dos registros de saúde


## 7. Propostas Rejeitadas (com Justificativa)

- **Rejeitado:** Implementar backup descentralizado via rede P2P (ex.: IPFS) com replicação em múltiplos nós controlados pelo usuário (Origem: ALTERNATIVES)
  *Motivo:* Requer configuração complexa, dependência de conectividade de rede e aumenta o consumo de armazenamento, contrariando a simplicidade desejada pelo usuário
- **Rejeitado:** Incorporar módulos de aprendizado de máquina on‑device para análise avançada de padrões de saúde (Origem: ALTERNATIVES)
  *Motivo:* Consome recursos de CPU/GPU, necessita de atualizações periódicas e aumenta a complexidade de desenvolvimento, o que pode ser excessivo para o objetivo inicial de privacidade e simplicidade


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Armazenamento local criptografado dos dados de saúde com backups automáticos para um drive externo criptografado controlado pelo usuário.)

**Dependências Externas do Core:**
- Disponibilidade de um drive externo (USB, SSD, etc.) que o usuário possa conectar ao dispositivo
- Suporte do sistema operacional ao acesso de arquivos em modo leitura/escrita ao drive externo sem elevação de privilégios excessiva
- API de criptografia segura e armazenamento de chaves fornecida pelo SO (ex.: Android Keystore, iOS Keychain, Windows DPAPI)
- Capacidade de agendar tarefas em background ou serviço que monitore alterações de dados para disparar o backup
- Mecanismo de montagem automática ou detecção de inserção do drive externo pelo SO

**Testes Discriminativos do Core:**
- [ ] Verificar que o arquivo de dados de saúde no armazenamento local está criptografado (comparar tamanho e entropia antes/depois)
- [ ] Simular a inserção de um drive externo e confirmar que o aplicativo detecta o dispositivo dentro de X segundos
- [ ] Executar a rotina de backup automático e inspecionar o arquivo copiado no drive externo para garantir que está criptografado
- [ ] Testar a restauração dos dados a partir do backup criptografado usando a chave armazenada no keystore
- [ ] Medir o tempo de gravação/leitura de dados criptografados versus não criptografados para validar impacto de desempenho aceitável


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Avaliar a precisão de reconhecimento de voz offline em diferentes ambientes ruidosos usando um modelo local pequeno
- [ ] *[EXPLORATÓRIO]* Testar a sincronização de dados de saúde com um wearable Bluetooth de baixa energia para garantir latência aceitável
- [ ] *[EXPLORATÓRIO]* Implementar um protótipo de backup descentralizado via rede P2P (ex.: IPFS) e medir taxa de sucesso de replicação em nós controlados pelo usuário
- [ ] *[EXPLORATÓRIO]* Executar um modelo de aprendizado de máquina on‑device para detecção de padrões de sintomas e comparar resultados com análise manual
- [ ] *[EXPLORATÓRIO]* Avaliar a usabilidade de formulários estruturados com validação automática de campos (ex.: unidades, limites fisiológicos)


## 10. Próximo Passo Recomendado

Desenvolver o mecanismo central de armazenamento criptografado com backup automático para um drive externo criptografado controlado pelo usuário, e conduzir testes de usabilidade para validar a confiabilidade do backup e a facilidade de uso para o usuário final.
