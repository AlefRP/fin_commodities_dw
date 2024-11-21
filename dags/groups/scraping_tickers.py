from airflow.decorators import task, task_group
from sqlalchemy.orm import Session
from .models.dim_commodity import DimCommodity
from .conf.db_config import criar_engine
import requests
from bs4 import BeautifulSoup
import logging

# Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@task.python(pool='scraping_pool')
def obter_lista_commodities():
    """
    Realiza scraping no Yahoo Finance para obter a lista de commodities.
    
    Returns:
        list: Uma lista de dicionários contendo 'ticker' e 'name'.
    """
    url = "https://finance.yahoo.com/commodities"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        logger.info("Realizando requisição para obter dados de commodities...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        tabela = soup.find('table')

        if not tabela:
            logger.warning("Nenhuma tabela encontrada na página.")
            return []

        commodities = []
        for row in tabela.find_all('tr')[1:]:
            cols = row.find_all('td')
            if len(cols) > 1:
                ticker = cols[0].text.strip()
                name = cols[1].text.strip()
                commodities.append({'ticker': ticker, 'name': name})

        logger.info(f"{len(commodities)} commodities encontradas.")
        return commodities

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro durante a requisição HTTP: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao processar a página: {e}")
        raise

@ task.python(do_xcom_push=False, pool='scraping_pool')
def carregar_dim_commodity(commodities: list, conn_str: str):
    """
    Insere os dados de commodities na tabela `dim_commodity`.
    
    Args:
        commodities (list): Lista de dicionários contendo dados das commodities.
        conn_str (str): String de conexão ao banco de dados.
    """
    try:
        engine = criar_engine(conn_str)

        if not commodities:
            logger.warning("Nenhuma commodity para processar. Encerrando execução.")
            return

        with Session(engine) as session:
            for commodity in commodities:
                ticker = commodity['ticker']
                name = commodity['name']
                categoria = "Desconhecido"

                if not session.query(DimCommodity).filter_by(ticker=ticker).first():
                    nova_commodity = DimCommodity(
                        nome=name,
                        ticker=ticker,
                        categoria=categoria
                    )
                    session.add(nova_commodity)
                    logger.info(f"Nova commodity adicionada: {name} ({ticker})")
                else:
                    logger.debug(f"Commodity já existente: {name} ({ticker})")

            session.commit()
            logger.info("Carga de dados concluída com sucesso!")

    except Exception as e:
        logger.error(f"Erro ao carregar a tabela `dim_commodity`: {e}")
        raise

@task_group
def scraper_tickers_commodities(conn_str: str):
    """
    Grupo de tarefas para processar os dados de commodities.
    
    Args:
        conn_str (str): String de conexão ao banco de dados.
    """
    commodities = obter_lista_commodities()
    carregar_dim_commodity(commodities, conn_str)

