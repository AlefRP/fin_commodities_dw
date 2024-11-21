import pytest
from airflow.models import DagBag
from unittest.mock import patch, MagicMock

@pytest.fixture(scope="module")
def dag_bag():
    return DagBag(dag_folder="caminho_para_seu_dag_folder", include_examples=False)

def test_dag_loaded(dag_bag):
    """Teste se a DAG é carregada corretamente."""
    dag = dag_bag.get_dag(dag_id="api_commodities")
    assert dag is not None
    assert len(dag.tasks) > 0

@patch("api_commodities.psycopg2.connect")
def test_verificar_tabelas_existentes(mock_connect):
    """Teste a lógica da tarefa 'verificar_tabelas_existentes'."""
    from dags.api_commodities import verificar_tabelas_existentes

    # Mock da conexão
    mock_cursor = MagicMock()
    mock_connect.return_value.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = [True]

    # Simular execução da tarefa
    conn_str = "mock_conn_str"
    result = verificar_tabelas_existentes(conn_str)

    assert result == "tabelas_existem"
