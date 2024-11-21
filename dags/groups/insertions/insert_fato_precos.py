from sqlalchemy.orm import Session
from groups.models.fato_precos import FatoPrecos

def insert_fato_precos(session: Session, data, commodity_id: int, mercado_id: int,
                       preco_abertura: float, preco_maximo: float, preco_minimo: float,
                       preco_fechamento: float, volume: int) -> None:
    """
    Insere dados na tabela `fato_precos`.

    Args:
        session (Session): Sessão SQLAlchemy.
        data (date): Data da entrada.
        commodity_id (int): ID da commodity.
        mercado_id (int): ID do mercado.
        preco_abertura (float): Preço de abertura.
        preco_maximo (float): Preço máximo.
        preco_minimo (float): Preço mínimo.
        preco_fechamento (float): Preço de fechamento.
        volume (int): Volume negociado.
    """
    fato = FatoPrecos(
        data=data,
        commodity_id=commodity_id,
        mercado_id=mercado_id,
        preco_abertura=preco_abertura,
        preco_maximo=preco_maximo,
        preco_minimo=preco_minimo,
        preco_fechamento=preco_fechamento,
        volume=volume
    )
    session.add(fato)
    session.commit()
