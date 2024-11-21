import logging
import pandas as pd
from airflow.decorators import task, task_group
from .conf.db_config import criar_sessao
from .insertions.insert_dim_calendario import insert_dim_calendario
from .insertions.insert_dim_commodity import insert_dim_commodity
from .insertions.insert_dim_mercado import insert_dim_mercado
from .insertions.insert_fato_precos import insert_fato_precos
from .models.dim_commodity import DimCommodity
from .models.dim_calendario import DimCalendario
from .models.dim_mercado import DimMercado
from datetime import datetime, timedelta
import yfinance as yf

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@task.python
def carregar_dim_calendario(conn_str):
    """
    Insere todas as datas dos últimos 4 anos na tabela `dim_calendario`.
    """
    try:
        with criar_sessao(conn_str) as session:
            logger.info("Inserindo datas dos últimos 4 anos na tabela DimCalendario...")
            data_atual = datetime.today().date()
            data_inicio = data_atual - timedelta(days=4 * 365)  # Calcula a data de 4 anos atrás

            # Gera todas as datas no intervalo
            while data_inicio <= data_atual:
                data_existe = session.query(DimCalendario).filter_by(data=data_inicio).first()
                if not data_existe:
                    insert_dim_calendario(session, data_inicio)
                data_inicio += timedelta(days=1)  # Incrementa para a próxima data

            logger.info("Todas as datas dos últimos 4 anos foram inseridas na tabela DimCalendario.")
    except Exception as e:
        logger.error(f"Erro ao carregar DimCalendario: {e}")

@task.python
def carregar_dim_commodity(conn_str):
    """
    Atualiza ou insere commodities na tabela `dim_commodity` com base nos tickers existentes.
    """
    try:
        with criar_sessao(conn_str) as session:
            logger.info("Iniciando processamento de DimCommodity...")

            commodities_existentes = session.query(DimCommodity).all()
            if not commodities_existentes:
                logger.warning("Nenhuma commodity existente encontrada na tabela `dim_commodity`.")
                return

            for commodity in commodities_existentes:
                try:
                    dados = yf.Ticker(commodity.ticker).info
                    categoria = dados.get("sector", "Desconhecido")
                    insert_dim_commodity(session, commodity.nome, commodity.ticker, categoria)
                except Exception as e:
                    logger.error(f"Erro ao processar {commodity.nome} ({commodity.ticker}): {e}")

            logger.info("DimCommodity processado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar DimCommodity: {e}")

@task.python
def carregar_dim_mercado(conn_str):
    """
    Insere ou atualiza mercados na tabela `dim_mercado`.
    """
    mercados = [
        {'nome': 'NYMEX', 'pais': 'Estados Unidos', 'moeda': 'USD'}
    ]
    try:
        with criar_sessao(conn_str) as session:
            logger.info("Iniciando processamento de DimMercado...")
            for mercado in mercados:
                try:
                    insert_dim_mercado(session, mercado['nome'], mercado['pais'], mercado['moeda'])
                except Exception as e:
                    logger.error(f"Erro ao processar mercado {mercado['nome']}: {e}")
            logger.info("DimMercado processado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar DimMercado: {e}")

@task.python
def carregar_fato_precos(conn_str):
    """
    Carrega dados históricos dos últimos 4 anos na tabela `fato_precos`.
    """
    try:
        with criar_sessao(conn_str) as session:
            logger.info("Iniciando processamento de FatoPrecos...")

            commodities = session.query(DimCommodity).all()
            mercado = session.query(DimMercado).filter_by(nome='NYMEX').first()
            if not mercado:
                raise ValueError("Mercado 'NYMEX' não encontrado na tabela `dim_mercado`.")

            for commodity in commodities:
                try:
                    logger.info(f"Obtendo dados históricos para {commodity.nome} ({commodity.ticker})...")

                    # Realiza múltiplas requisições para cobrir os últimos 4 anos
                    data_inicio = datetime.today() - timedelta(days=4 * 365)
                    data_fim = datetime.today()

                    # Inicializa um DataFrame vazio
                    dados_completos = None

                    # Solicita dados para cada ano
                    for ano in range(4):
                        data_fim_periodo = data_inicio + timedelta(days=365)
                        periodo_dados = yf.Ticker(commodity.ticker).history(
                            start=data_inicio.strftime('%Y-%m-%d'),
                            end=data_fim_periodo.strftime('%Y-%m-%d'),
                            interval="1d"
                        ).reset_index()

                        # Concatena os dados
                        if dados_completos is None:
                            dados_completos = periodo_dados
                        else:
                            dados_completos = pd.concat([dados_completos, periodo_dados])

                        data_inicio = data_fim_periodo

                    # Itera sobre os dados consolidados
                    for _, row in dados_completos.iterrows():
                        data = row['Date'].date()

                        # Garante que a data exista na tabela DimCalendario
                        carregar_dim_calendario(conn_str)

                        # Insere os dados na tabela fato_precos
                        insert_fato_precos(
                            session,
                            data,
                            commodity_id=commodity.id,
                            mercado_id=mercado.id,
                            preco_abertura=row['Open'],
                            preco_maximo=row['High'],
                            preco_minimo=row['Low'],
                            preco_fechamento=row['Close'],
                            volume=row['Volume']
                        )
                except Exception as e:
                    session.rollback()
                    logger.error(f"Erro ao processar dados históricos para {commodity.nome} ({commodity.ticker}): {e}")

            logger.info("FatoPrecos processado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao carregar FatoPrecos: {e}")


@task_group
def carregar_dimensoes(conn_str):
    carregar_dim_calendario(conn_str)
    carregar_dim_commodity(conn_str)
    carregar_dim_mercado(conn_str)
