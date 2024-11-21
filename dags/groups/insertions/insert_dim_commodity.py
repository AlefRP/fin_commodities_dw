from sqlalchemy.orm import Session
from groups.models.dim_commodity import DimCommodity

def insert_dim_commodity(session: Session, nome: str, ticker: str, categoria: str) -> int:
    """
    Insere uma nova commodity na tabela `dim_commodity` ou atualiza a categoria se o registro já existir.

    Args:
        session (Session): Sessão SQLAlchemy.
        nome (str): Nome da commodity.
        ticker (str): Ticker da commodity.
        categoria (str): Categoria da commodity.

    Returns:
        int: ID da commodity inserida ou existente.
    """
    # Verifica se o registro já existe
    commodity = session.query(DimCommodity).filter_by(
        nome=nome,
        ticker=ticker
    ).first()

    if commodity:
        # Atualiza a categoria se for diferente
        if commodity.categoria != categoria:
            commodity.categoria = categoria
            session.commit()
            print(f"Categoria atualizada para o registro existente: {commodity.id}")
        return commodity.id

    # Insere um novo registro se não existir
    commodity = DimCommodity(nome=nome, ticker=ticker, categoria=categoria)
    session.add(commodity)
    session.commit()
    session.refresh(commodity)
    print(f"Novo registro inserido: {commodity.id}")
    return commodity.id
