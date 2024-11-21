from airflow.decorators import dag, task, task_group
from airflow.models import Variable
from addins.decorators import custom_task
from groups.criar_tabelas import criar_dim, criar_tabela_fato_precos
from groups.scraping_tickers import scraper_tickers_commodities
from groups.carregar_dados import carregar_dimensoes, carregar_fato_precos
from groups.conf.db_config import definir_str_conexao_postgres
from datetime import datetime
import psycopg2

def configurar_conexao():
    """
    Configura a string de conexão para o banco de dados.
    Retorna a string.
    """
    return definir_str_conexao_postgres(
        host=Variable.get("postgres_dw_host"),
        porta=int(Variable.get("postgres_dw_port")),
        usuario=Variable.get("postgres_dw_user"),
        senha=Variable.get("postgres_dw_password"),
        nome_bd=Variable.get("postgres_dw_db"),
    )

default_args = {
    'start_date': datetime(2024, 1, 1)
}

@dag(
    default_args=default_args,
    schedule_interval=None,
    tags=['commodities', 'engenharia_de_dados'],
    catchup=False,
)
def api_commodities():
    """
    DAG para criar tabelas do Data Warehouse.
    Configura a conexão ao banco de dados e executa
    as tarefas de criação de dimensões e tabela fato.
    """

    @custom_task.empty
    def inicio():
        """Tarefa inicial do DAG."""
        pass

    @custom_task.empty
    def fim():
        """Tarefa final do DAG."""
        pass

    @task.python(do_xcom_push=True)
    def obter_conexao():
        """
        Obtém a string de conexão para o banco de dados.
        Esta função será executada em tempo de execução.
        """
        conn = configurar_conexao()
        return conn

    @task.branch(task_id="verificar_tabelas_existentes")
    def verificar_tabelas_existentes(conn_str: str):
        """
        Verifica a existência das tabelas no banco de dados e decide o fluxo.
        Retorna a ID da próxima tarefa a ser executada.
        """
        tabelas = ['dim_calendario', 'dim_commodity', 'dim_mercado', 'fato_precos']
        try:
            conn = psycopg2.connect(conn_str)
            cursor = conn.cursor()
            tabelas_existentes = []
            for tabela in tabelas:
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT 1
                        FROM information_schema.tables
                        WHERE table_name = '{tabela}'
                    );
                """)
                if cursor.fetchone()[0]:
                    tabelas_existentes.append(tabela)
            conn.close()
            if len(tabelas_existentes) == len(tabelas):
                return "tabelas_existem"
            else:
                return "criar_tabelas"
        except Exception as e:
            raise RuntimeError(f"Erro ao verificar tabelas: {e}")

    @custom_task.empty
    def tabelas_existem():
        """Tarefa que indica que as tabelas já existem."""
        pass

    @task_group(group_id='criar_tabelas')
    def criar_tabelas(conn_str: str):
        criar_dim_task = criar_dim(conn_str)
        criar_fato_task = criar_tabela_fato_precos(conn_str)
        
        criar_dim_task >> criar_fato_task

    @task_group(group_id='carregar_dados')
    def carregar_dados(conn_str: str):
        scraper_tickers_commodities(conn_str)
        carregar_dimensoes(conn_str)
        carregar_fato_precos(conn_str)
        @custom_task.empty(task_id="carregar_dados_final", trigger_rule="none_failed_or_skipped")
        def finalizar_carregar_dados():
            """Finalizador do grupo carregar_dados."""
            pass
        return finalizar_carregar_dados()

    # Criação das tarefas e grupos
    inicio_task = inicio()
    fim_task = fim()
    conn_str_task = obter_conexao()
    verificar_tabelas_task = verificar_tabelas_existentes(conn_str_task)
    tabelas_existem_task = tabelas_existem()
    criar_tabelas_task = criar_tabelas(conn_str_task)
    carregar_dados_task = carregar_dados(conn_str_task)

    # Definindo as dependências
    inicio_task >> conn_str_task >> verificar_tabelas_task
    verificar_tabelas_task >> [tabelas_existem_task, criar_tabelas_task]
    tabelas_existem_task >> carregar_dados_task
    criar_tabelas_task >> carregar_dados_task >> fim_task

dag = api_commodities()
