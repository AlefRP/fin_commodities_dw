import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.future.engine import Engine
from typing import Optional

# Instância do engine global
__engine: Optional[Engine] = None

def definir_str_conexao_postgres(host: str, porta: int, usuario: str, senha: str, nome_bd: str) -> str:
    """
    Define a string de conexão para o PostgreSQL.

    Args:
        host (str): Endereço do host.
        porta (int): Porta do servidor PostgreSQL.
        usuario (str): Usuário do banco de dados.
        senha (str): Senha do usuário.
        nome_bd (str): Nome do banco de dados.

    Returns:
        str: String de conexão gerada.
    """
    _postgres_conn_str = f"postgresql://{usuario}:{senha}@{host}:{porta}/{nome_bd}"
    print(f"String de conexão configurada: {_postgres_conn_str}")
    return _postgres_conn_str

def criar_engine(_postgres_conn_str: str) -> Engine:
    """
    Cria e retorna o engine de conexão com o PostgreSQL.

    Args:
        _postgres_conn_str (str): String de conexão com o PostgreSQL.

    Returns:
        Engine: Engine SQLAlchemy conectado ao PostgreSQL.
    """
    global __engine

    if __engine:
        return __engine

    if not _postgres_conn_str:
        raise ValueError("A string de conexão não foi definida. Use 'definir_str_conexao_postgres'.")

    __engine = sa.create_engine(url=_postgres_conn_str, echo=False)
    return __engine

def criar_sessao(_postgres_conn_str: str) -> Session:
    """
    Cria e retorna uma sessão SQLAlchemy para o banco de dados.

    Args:
        _postgres_conn_str (str): String de conexão com o PostgreSQL.

    Returns:
        Session: Objeto de sessão SQLAlchemy.
    """
    engine = criar_engine(_postgres_conn_str)
    SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessaoLocal()
