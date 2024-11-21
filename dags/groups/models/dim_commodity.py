import sqlalchemy as sa
from .model_base import ModelBase

class DimCommodity(ModelBase):
    """
    Dimensão que representa as commodities.
    """
    __tablename__ = 'dim_commodity'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    nome = sa.Column(sa.String(50), nullable=False, unique=True)
    ticker = sa.Column(sa.String(10), nullable=False, unique=True)
    categoria = sa.Column(sa.String(50), nullable=False)

    def __repr__(self):
        return f"<DimCommodity(nome={self.nome}, ticker={self.ticker}, categoria={self.categoria})>"
