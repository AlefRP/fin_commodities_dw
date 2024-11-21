# Execução do Projeto

## Introdução

Este documento fornece instruções detalhadas sobre como configurar o ambiente e executar o projeto MERX, garantindo que todas as dependências e requisitos sejam atendidos de forma adequada.

## Requisitos

- **Docker**: O Docker é necessário para criar e gerenciar os containers do projeto. Certifique-se de que o Docker esteja instalado e configurado na sua máquina.
- **Astro CLI**: O Astro CLI é utilizado para gerenciar o Airflow e executar as DAGs localmente. Instruções de instalação podem ser encontradas [aqui](https://www.astronomer.io/docs/astro/cli/install-cli/).
- **Python 3.8+**: Certifique-se de ter a versão adequada do Python instalada para rodar scripts auxiliares.

## Configuração do Ambiente

1. **Clonar o Repositório**
   - Clone o repositório do projeto utilizando o comando abaixo:

     ```bash
     git clone https://github.com/seu-usuario/merx-case.git
     cd merx-case
     ```

2. **Configurar o Airflow**
   - Inicialize o banco de dados do Airflow e inicie o servidor local:

     ```bash
     astro dev start
     ```

## Execução de Tarefas em Ambiente Isolado

Como o projeto utiliza o Astro CLI que utiliza o Docker por baixo dos panos, o projeto em sí já funciona em uma camada de isolamento não sendo necessário o uso de ambiente virtual. Para tarefas que necessitam de um ambiente isolado, pode-se utilizar o decorator `@task.external_python` ou o `ExternalPythonOperator` do Airflow (O que não foi utilizado no projeto, apenas para informação). Isso permite executar tarefas em um ambiente Python separado, garantindo isolamento para dependências específicas. 

Exemplos de uso:

  ```python
  from airflow.decorators import task
  from airflow.providers.common.sql.operators.external_python import ExternalPythonOperator

  @task.external_python(python='/path/to/venv/bin/python')
  def tarefa_isolada():
      # Código da tarefa isolada
      pass

  external_task = ExternalPythonOperator(
      task_id='external_task',
      python='/path/to/venv/bin/python',
      python_callable=tarefa_isolada
  )
  ```

Certifique-se de configurar o caminho correto para o ambiente Python desejado (que deve ser instalado no ambiente docker atualizando-se o `Dockerfile`).

## Executando o Projeto

- **Inicializar o Airflow**: Após iniciar o servidor com `astro dev start`, acesse a interface web do Airflow em `http://localhost:8080`.
- **Variáveis e Conexões**: Certifique-se de configurar todas as variáveis e conexões necessárias na interface do Airflow.
  - As variáveis para acessar o Data Warehouse no PostgreSQL estão definidas no arquivo `.env`. Para acessar o DW, utilize um cliente de banco de dados como o DBeaver e as seguintes informações de acesso:
  
    ```txt
    HOST=localhost
    PORTA=5434
    USUARIO=user_dw
    SENHA=1234
    BANCO_DE_DADOS=commodities_dw
    ```

  - Ao baixar o projeto e usar o comando `astro dev start`, o servidor de banco de dados adicional já é criado automaticamente devido a especificação do `docker-compose.override.yml`. Não é necessário nenhuma configuração adicional. Apenas visite a UI do Airflow e execute a DAG.

- **Rodar a DAG Principal**: Navegue até o painel do Airflow e ative a DAG chamada `api_commodities`. Esta DAG é responsável por automatizar a coleta, transformação e armazenamento dos dados.

  - Também é possível definir variaveis, pools e conexões no arquivo no arquivo `airflow_settings.yaml`. Foram criadas algumas conexões apenas para demonstração, elas não são utilizadas no projeto, com execção das pools que de fato são utilizadas.

O Airflow cria um Data Warehouse modelado em **SQLAlchemy** utilizando o padrão **Star Schema**, com as seguintes tabelas:

- **`dim_calendario`**
- **`dim_commodity`**
- **`dim_mercado`**
- **`fato_precos`**

Um **Branch Operator** verifica se as tabelas já existem no banco de dados. Caso existam, as tasks de carga de dados são executadas diretamente. Caso contrário, a criação das tabelas é feita antes de continuar.

Os modelos do SQLAlchemy estão localizados em: `dags/groups/models`.

## Coleta e Carga de Dados

1. **Scraper de Tickers**
   - Um script utilizando **Beautiful Soup** realiza o scraper dos tickers de commodities diretamente do Yahoo Finance, carregando os resultados na tabela `dim_commodity`.

2. **Coleta de Dados**
   - Um segundo script utiliza os tickers extraídos para consultar a **API do Yahoo** e carregar os preços das commodities na tabela `fato_precos`.

## Testes

- **Testes Automatizados**: Os testes foram implementados utilizando `pytest`. Para executar os testes e garantir que todas as funcionalidades estejam funcionando corretamente, utilize o comando:

  ```bash
  pytest tests/dags/test_api_commodities.py
  ```

## Conclusão

Certifique-se de seguir todas as etapas descritas acima para configurar corretamente o ambiente. O projeto MERX está pronto para ser executado e explorado.
