from sqlalchemy.orm import Session
from groups.models.dim_mercado import DimMercado

def insert_dim_mercado(session: Session, nome: str, pais: str, moeda: str) -> int:
    """
    Insere um novo mercado na tabela `dim_mercado` ou retorna o ID existente.

    Args:
        session (Session): Sessão SQLAlchemy.
        nome (str): Nome do mercado.
        pais (str): País do mercado.
        moeda (str): Moeda do mercado.

    Returns:
        int: ID do mercado inserido ou existente.
    """
    mercado = session.query(DimMercado).filter_by(nome=nome, pais=pais, moeda=moeda).first()
    if mercado:
        return mercado.id

    mercado = DimMercado(nome=nome, pais=pais, moeda=moeda)
    session.add(mercado)
    session.commit()
    session.refresh(mercado)
    return mercado.id
