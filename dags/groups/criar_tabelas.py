from airflow.decorators import task, task_group
from .models.model_base import ModelBase
from .models import dim_calendario, dim_commodity, dim_mercado, fato_precos
from .conf.db_config import criar_engine


@task.python
def dropar_tabelas(_postgres_conn_str):
    """
    Dropar todas as tabelas existentes no metadata do ModelBase.
    """
    engine = criar_engine(_postgres_conn_str)
    ModelBase.metadata.drop_all(bind=engine)

@task.python
def criar_tabela_dim_commodity(_postgres_conn_str):
    """
    Criar a tabela DimCommodity, se ainda não existir.
    """
    engine = criar_engine(_postgres_conn_str)
    dim_commodity.DimCommodity.__table__.create(bind=engine, checkfirst=True)

@task.python
def criar_tabela_dim_mercado(_postgres_conn_str):
    """
    Criar a tabela DimMercado, se ainda não existir.
    """
    engine = criar_engine(_postgres_conn_str)
    dim_mercado.DimMercado.__table__.create(bind=engine, checkfirst=True)

@task.python
def criar_tabela_dim_tempo(_postgres_conn_str):
    """
    Criar a tabela DimCalendario, se ainda não existir.
    """
    engine = criar_engine(_postgres_conn_str)
    dim_calendario.DimCalendario.__table__.create(bind=engine, checkfirst=True)

@task.python
def criar_tabela_fato_precos(_postgres_conn_str):
    """
    Criar a tabela FatoPrecos, se ainda não existir.
    """
    engine = criar_engine(_postgres_conn_str)
    fato_precos.FatoPrecos.__table__.create(bind=engine, checkfirst=True)

@task_group
def criar_dim(_postgres_conn_str):
    """
    Grupo de tarefas para criar as tabelas de dimensão.
    Recebe a string de conexão como argumento.
    """
    criar_tabela_dim_commodity(_postgres_conn_str=_postgres_conn_str)
    criar_tabela_dim_mercado(_postgres_conn_str=_postgres_conn_str)
    criar_tabela_dim_tempo(_postgres_conn_str=_postgres_conn_str)
