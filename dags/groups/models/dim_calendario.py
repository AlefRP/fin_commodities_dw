import sqlalchemy as sa
from .model_base import ModelBase

class DimCalendario(ModelBase):
    """
    Dimensão que representa as datas e períodos.
    """
    __tablename__ = 'dim_calendario'

    data = sa.Column(sa.Date, primary_key=True, unique=True)
    ano = sa.Column(sa.Integer, nullable=False)
    mes = sa.Column(sa.Integer, nullable=False)
    dia = sa.Column(sa.Integer, nullable=False)
    trimestre = sa.Column(sa.Integer, nullable=False)

    def __repr__(self):
        return f"<DimCalendario(data={self.data}, ano={self.ano}, mes={self.mes}, dia={self.dia}, trimestre={self.trimestre})>"
