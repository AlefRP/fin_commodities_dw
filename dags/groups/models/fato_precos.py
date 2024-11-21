import sqlalchemy as sa
from .model_base import ModelBase

class FatoPrecos(ModelBase):
    """
    Tabela fato que armazena preços e volumes de commodities.
    """
    __tablename__ = 'fato_precos'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    data = sa.Column(sa.Date, sa.ForeignKey('dim_calendario.data'), nullable=False)
    commodity_id = sa.Column(sa.Integer, sa.ForeignKey('dim_commodity.id'), nullable=False)
    mercado_id = sa.Column(sa.Integer, sa.ForeignKey('dim_mercado.id'), nullable=False)
    preco_abertura = sa.Column(sa.Float, nullable=False)
    preco_maximo = sa.Column(sa.Float, nullable=False)
    preco_minimo = sa.Column(sa.Float, nullable=False)
    preco_fechamento = sa.Column(sa.Float, nullable=False)
    volume = sa.Column(sa.BigInteger, nullable=True)

    def __repr__(self):
        return (
            f"<FatoPrecos(data={self.data}, commodity_id={self.commodity_id}, mercado_id={self.mercado_id}, "
            f"preco_abertura={self.preco_abertura}, preco_fechamento={self.preco_fechamento}, volume={self.volume})>"
        )
