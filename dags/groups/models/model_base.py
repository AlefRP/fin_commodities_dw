from sqlalchemy.orm import declarative_base

Base = declarative_base()

class ModelBase(Base):
    """
    Classe base abstrata para os modelos do SQLAlchemy.
    Não define colunas diretamente, mas fornece a base para outros modelos.
    """
    __abstract__ = True
