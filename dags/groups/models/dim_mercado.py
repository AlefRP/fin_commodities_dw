import sqlalchemy as sa
from .model_base import ModelBase

class DimMercado(ModelBase):
    """
    Dimensão que representa o mercado onde a commodity é negociada.
    """
    __tablename__ = 'dim_mercado'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nome = sa.Column(sa.String(50), nullable=False, unique=True)
    pais = sa.Column(sa.String(50), nullable=False)
    moeda = sa.Column(sa.String(10), nullable=False)

    def __repr__(self):
        return f"<DimMercado(nome={self.nome}, pais={self.pais}, moeda={self.moeda})>"
