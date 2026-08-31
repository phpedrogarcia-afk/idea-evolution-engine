# Baseline de Refinamento de Ideia — EXP-M05.4-IDEA-04-COND-A

## Ideia Original
> Um gerador de relatórios financeiros pessoais que precisa funcionar 100% offline, em um único arquivo HTML local, sem banco de dados externo e sem login.

## Resumo do Modelo
Um gerador de relatórios financeiros pessoais totalmente offline, implementado como um único arquivo HTML que utiliza recursos nativos do navegador (JavaScript, IndexedDB/localStorage, Service Workers) para armazenar dados, processar cálculos e gerar relatórios visualmente ricos, exportáveis em PDF ou CSV, sem necessidade de login ou servidores externos.

## Versão Refinada
Um aplicativo web single‑page (SPA) em um único arquivo HTML que usa JavaScript puro ou frameworks leves para: 
1. Importar dados financeiros via arquivos CSV/Excel arrastando‑e‑soltando; 
2. Armazenar temporariamente os registros em IndexedDB com opção de criptografia opcional; 
3. Processar cálculos (receitas, despesas, categorias, projeções) totalmente no cliente; 
4. Gerar relatórios interativos com gráficos (Chart.js) e tabelas estilizadas; 
5. Exportar relatórios como PDF (via jsPDF) ou CSV; 
6. Utilizar Service Worker para garantir funcionamento offline completo; 
7. Oferecer um modo "sandbox" que salva tudo em memória apenas enquanto a página está aberta, para usuários que não desejam persistência. Tudo isso sem necessidade de login, servidores ou bancos de dados externos.

## Pontos Fortes e Fracos
- **Fortes:** Privacidade total – nenhum dado sai do dispositivo do usuário, Operação 100% offline – útil em ambientes sem conexão, Instalação simples – basta abrir o arquivo HTML, Baixo custo de desenvolvimento e manutenção, Portabilidade – pode ser copiado e usado em qualquer computador
- **Fracos:** Capacidade de armazenamento limitada ao espaço disponível no navegador, Gerenciamento de dados complexo pode ser difícil sem um DB tradicional, Risco de perda de dados se o usuário limpar o cache do navegador, Funcionalidades avançadas (ex.: integração bancária) são inviáveis offline, Segurança dos dados depende de criptografia client‑side, que pode ser frágil

## Próximos Passos
Definir requisitos detalhados (tipos de relatórios, filtros, exportação), Escolher bibliotecas JavaScript (Chart.js, jsPDF, IndexedDB wrapper), Desenhar wireframes da interface de usuário e fluxo de importação/exportação, Implementar protótipo básico: importação CSV, armazenamento em IndexedDB, cálculo simples e visualização de gráfico, Adicionar funcionalidade de exportação PDF/CSV e opções de criptografia opcional, Testar o aplicativo em diferentes navegadores e cenários offline, Documentar instruções de uso e procedimentos de backup/restauração de dados, Coletar feedback de usuários piloto e iterar melhorias
