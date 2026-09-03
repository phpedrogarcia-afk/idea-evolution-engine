# Pacote de Maturação da Ideia — Run EXP-M05.5R2-H05-COND-B

**Status:** `REFINEMENT_INCOMPLETE` | **Ciclos de Reconstrução:** 1

---

## 1. Ideia Original (Imutável)

> No galpão onde fazemos reparos de bicicletas, perdemos muito tempo procurando ferramentas que foram usadas em outro canto ou ficaram em bicicletas prontas. Pensei em criar um jeito físico e prático de saber onde as ferramentas importantes estão durante o dia.


## 2. Intenção Humana & Problema Definido

- **Intenção Preservada:** Criar um método físico e prático para saber, a qualquer momento, onde as ferramentas importantes estão localizadas durante o dia.
- **Problema Central:** Perda de tempo ao procurar ferramentas que foram deixadas em locais diferentes ou em bicicletas prontas dentro do galpão de reparos.
- **Atores / Usuários:** Mecânicos de bicicletas, Assistentes de oficina, Gerente da oficina


## 3. Versão Refinada e Mecanismo Proposto

Um quadro de sombras magnético com compartimentos coloridos e registro visual de entrada/saída para localizar rapidamente as ferramentas essenciais durante o dia.


- **Justificativa de Promoção ao Core:** Fornece um método físico, imediato e de baixo custo que atende à intenção humana de saber onde as ferramentas estão, sem depender de energia ou dispositivos eletrônicos. (Base: `MODEL_HYPOTHESIS`)


## 4. Vulnerabilidades e Críticas Severas Encontradas

1. **[HIGH]** Dependência excessiva da conformidade dos usuários ao devolver ferramentas ao local designado
   - *Impacto:* Se os mecânicos não seguirem consistentemente o novo procedimento, o sistema perde sua utilidade e o tempo gasto na busca não será reduzido
   - *Parte Afetada:* Comportamento dos usuários / processos operacionais
2. **[MEDIUM]** Etiquetagem física de cada ferramenta pode ser trabalhosa e sujeita a desgaste
   - *Impacto:* A manutenção das etiquetas aumenta o custo operacional e pode tornar o sistema inutilizável quando as marcas desaparecem
   - *Parte Afetada:* Etiquetagem das ferramentas
3. **[HIGH]** O sistema proposto assume que a localização das ferramentas é estática durante o dia
   - *Impacto:* Em um ambiente de reparo, as ferramentas são frequentemente movidas entre bicicletas, tornando um rastreamento estático ineficaz
   - *Parte Afetada:* Mecanismo de rastreamento de ferramentas
4. **[MEDIUM]** Instalação de suportes ou quadros pode obstruir o espaço de trabalho e criar riscos de segurança
   - *Impacto:* Obstruções podem aumentar o risco de acidentes e reduzir a eficiência ao invés de melhorá‑la
   - *Parte Afetada:* Layout do galpão


## 5. Mecanismos Alternativos Considerados

1. **Mecanismo:** Etiquetar cada ferramenta com um chip RFID passivo e instalar um leitor central no quadro de sombras; o leitor detecta automaticamente a presença e a ausência de cada ferramenta, atualizando um display digital em tempo real
   - *Tradeoffs:* Custo inicial dos chips RFID e do leitor central, Necessidade de alimentação elétrica para o leitor e o display, Possível interferência em ambientes com muito metal
2. **Mecanismo:** Acoplar pequenos beacons Bluetooth Low Energy (BLE) a cada ferramenta e desenvolver um aplicativo móvel que mostra a localização aproximada baseada na intensidade do sinal, permitindo ao usuário localizar rapidamente a ferramenta usando o smartphone
   - *Tradeoffs:* Vida útil da bateria dos beacons requer substituição periódica, Precisão limitada em ambientes com obstáculos metálicos ou paredes, Dependência de um smartphone ou tablet para visualização
3. **Mecanismo:** Instalar uma câmera de visão geral acima da bancada e usar software de visão computacional para reconhecer ferramentas por forma ou cor, exibindo sua posição em um painel ou aplicativo; as ferramentas podem ter marcadores visuais simples (ex.: adesivos de alto contraste) ao invés de etiquetas tradicionais
   - *Tradeoffs:* Custo e complexidade de instalação da câmera e do software de IA, Sensibilidade a variações de iluminação e necessidade de manutenção dos marcadores visuais, Preocupações com privacidade e necessidade de processamento em tempo real


## 6. Possibilidades Candidatas (Não Incorporadas ao Core)

1. *[CANDIDATE]* Etiquetar cada ferramenta com um chip RFID passivo e instalar um leitor central no quadro de sombras, atualizando um display digital em tempo real
2. *[CANDIDATE]* Acoplar pequenos beacons Bluetooth Low Energy (BLE) a cada ferramenta e usar um aplicativo móvel para localizar a ferramenta aproximada
3. *[CANDIDATE]* Instalar uma câmera de visão geral acima da bancada e usar software de visão computacional para reconhecer ferramentas por forma ou cor, exibindo sua posição em um painel


## 8. Dependências da Realidade & Testes Empíricos Necessários (CORE: Quadro de sombras magnético com compartimentos coloridos e registro visual)

**Dependências Externas do Core:**
- Disponibilidade de material magnético suficientemente forte para segurar as ferramentas previstas
- Materiais de divisão (plástico, madeira, metal) que possam ser coloridos e sejam duráveis
- Um método de registro visual confiável (ex.: painel transparente, câmera de baixa resolução ou sensores de presença) que possa ser integrado ao quadro
- Iluminação adequada na bancada para que as sombras ou indicadores visuais sejam claramente perceptíveis

**Testes Discriminativos do Core:**
- [ ] Teste de força magnética: medir a carga máxima que cada compartimento suporta antes de soltar a ferramenta (usar dinamômetro)
- [ ] Teste de visibilidade: avaliar a clareza das sombras ou indicadores sob diferentes condições de iluminação (luz natural, fluorescente, LED)
- [ ] Teste de tempo de localização: comparar o tempo médio de encontrar uma ferramenta usando o quadro de sombras versus um arranjo aleatório
- [ ] Teste de durabilidade: ciclo de inserção/remoção de ferramentas por 10 000 vezes e monitorar perda de força magnética


## 9. Testes Exploratórios Opcionais (Extensões Candidatas / Não-Core)

- [ ] *[EXPLORATÓRIO]* Avaliar a precisão de um leitor RFID central integrado ao quadro para atualizar automaticamente o display digital
- [ ] *[EXPLORATÓRIO]* Medir a latência e a precisão de localização baseada em beacons BLE acoplados a cada ferramenta usando um aplicativo móvel
- [ ] *[EXPLORATÓRIO]* Desenvolver e testar algoritmo de visão computacional a partir de uma câmera acima da bancada para reconhecer ferramentas marcadas com adesivos de alto contraste


## 10. Próximo Passo Recomendado

Construir um protótipo de pequeno porte do quadro de sombras magnético, testar com os mecânicos por uma semana e medir a taxa de devolução correta das ferramentas.
