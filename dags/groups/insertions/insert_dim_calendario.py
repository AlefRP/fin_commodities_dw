from sqlalchemy.orm import Session
from groups.models.dim_calendario import DimCalendario
from datetime import datetime, timedelta

def insert_dim_calendario(session: Session, data) -> None:
    """
    Insere uma nova entrada na tabela `dim_calendario` e preenche todas as datas
    do ano da data inserida, caso ainda não estejam na tabela.

    Args:
        session (Session): Sessão SQLAlchemy.
        data (date): Data a ser inserida.
    """
    # Extrair o ano da data fornecida
    ano = data.year

    # Verifica se todas as datas do ano já estão na tabela
    existe_ano = session.query(DimCalendario).filter_by(ano=ano).first()
    if not existe_ano:
        print(f"Preenchendo todas as datas do ano {ano}...")
        preencher_datas_ano(session, ano)

    # Insere a data fornecida, caso não exista
    calendario = session.query(DimCalendario).filter_by(data=data).first()
    if not calendario:
        calendario = DimCalendario(
            data=data,
            ano=data.year,
            mes=data.month,
            dia=data.day,
            trimestre=(data.month - 1) // 3 + 1
        )
        session.add(calendario)
        session.commit()


def preencher_datas_ano(session: Session, ano: int) -> None:
    """
    Preenche todas as datas de um ano na tabela `dim_calendario`.

    Args:
        session (Session): Sessão SQLAlchemy.
        ano (int): Ano a ser preenchido.
    """
    data_inicio = datetime(ano, 1, 1)
    data_fim = datetime(ano, 12, 31)
    delta = timedelta(days=1)

    while data_inicio <= data_fim:
        # Verifica se a data já está na tabela
        existente = session.query(DimCalendario).filter_by(data=data_inicio.date()).first()
        if not existente:
            # Insere a data
            calendario = DimCalendario(
                data=data_inicio.date(),
                ano=data_inicio.year,
                mes=data_inicio.month,
                dia=data_inicio.day,
                trimestre=(data_inicio.month - 1) // 3 + 1
            )
            session.add(calendario)
        data_inicio += delta

    session.commit()
    print(f"Todas as datas do ano {ano} foram preenchidas com sucesso!")
