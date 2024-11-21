# Governança de Dados

## Introdução

Este documento descreve as práticas de governança de dados implementadas no projeto MERX, incluindo estratégias para controle de qualidade, auditoria dos dados e segurança das informações. A governança de dados é essencial para garantir a integridade, a consistência e a disponibilidade dos dados em todo o ciclo de vida do projeto.

## Controle de Qualidade

- **Validação dos Dados**: Foram implementadas validações em cada etapa do pipeline ETL para garantir que os dados coletados e transformados estejam corretos e completos. Isso inclui a verificação de formatos, tipos de dados e valores esperados.
- **Tratamento de Erros**: Em caso de inconsistências, os registros incorretos são isolados e armazenados para análise posterior, enquanto os dados válidos continuam sendo processados.
- **Métricas de Qualidade**: Indicadores foram definidos para medir a qualidade dos dados em termos de completude, consistência e precisão. Esses indicadores são monitorados e utilizados para identificar pontos de melhoria no processo.

## Auditoria dos Dados

- **Logs de Execução**: Todos os processos do pipeline, incluindo ingestão, transformação e carregamento, são registrados em logs detalhados. Esses logs incluem informações sobre o status de cada tarefa, o tempo de execução e possíveis erros.
- **Rastreamento de Alterações**: Cada modificação nos dados é rastreada, possibilitando a identificação de quem realizou a alteração, quando foi feita e qual foi o impacto nos dados.
- **Monitoramento de Atividades**: O Airflow fornece uma interface gráfica que permite monitorar visualmente as atividades das DAGs, facilitando a auditoria dos processos e a identificação de falhas.

## Segurança dos Dados

- **Controle de Acesso**: O acesso ao banco de dados é restrito e gerenciado por meio de credenciais seguras. Apenas usuários autorizados têm permissão para acessar e modificar os dados.
- **Uso de Variáveis de Ambiente**: Credenciais sensíveis, como senhas de banco de dados, são armazenadas em variáveis de ambiente e não no código fonte, garantindo maior segurança.
- **Criptografia**: As conexões com o banco de dados utilizam criptografia para proteger os dados em trânsito, garantindo que informações sensíveis não sejam expostas durante a comunicação entre os sistemas.

## Conclusão

As práticas de governança de dados adotadas no projeto garantem que os dados sejam tratados com segurança, qualidade e transparência. Isso proporciona uma base confiável para a tomada de decisões e para o crescimento do projeto de forma sustentável.
