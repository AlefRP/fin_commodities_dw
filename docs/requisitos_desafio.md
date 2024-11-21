# Requisitos do Desafio

## Desafio de Seleção da MERX

Este documento detalha os requisitos do desafio prático de seleção para o cargo de Analista/Engenheiro de Dados na MERX. O desafio foi dividido em várias etapas, abrangendo desde a ingestão de dados até o processamento e documentação.

### 1. Ingestão de Dados

- Desenvolver um ambiente virtual para execução do projeto, incluindo a instalação do Apache Airflow.
- Criar uma DAG no Apache Airflow com duas tarefas principais:
  - **Inserção de Dados via Web Scraping**: Coletar dados de uma fonte pública utilizando técnicas de scraping e inseri-los no banco de dados.
  - **Integração com API**: Utilizar uma API pública para coletar dados e armazená-los no banco de dados.
- O banco de dados relacional utilizado deve ser PostgreSQL.
- Implementar mecanismos de tratamento de erros e garantir a reexecução dos processos.

### 2. Processamento e Transformação (ETL/ELT)

- Desenvolver um pipeline de ETL para pré-processar os dados coletados, realizando transformações como limpeza, normalização de formatos e conversão de tipos.
- Incluir uma etapa de validação para garantir que os dados estejam corretos antes de prosseguir para as próximas etapas.
- Utilizar o Airflow ou dbt para gerenciar a execução do pipeline.

### 3. Migração em Tempo Real (Opcional)

- Configurar um processo de ingestão contínua de dados utilizando ferramentas como Debezium ou AWS DMS, para simular a migração de dados em tempo real.

### 4. Documentação e Governança

- Documentar detalhadamente o pipeline criado, explicando as decisões tomadas em cada etapa.
- Incluir aspectos de governança de dados, como controle de qualidade, auditoria e segurança.

### 5. Entrega do Projeto

- O candidato deve fornecer o código e a documentação em um repositório git ou em um arquivo compactado.
