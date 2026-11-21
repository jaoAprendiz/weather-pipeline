import logging
import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

env_path = Path(__file__).resolve().parent.parent.parent / "config" / ".env"
load_dotenv(env_path)


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Variável de ambiente obrigatória não definida: {name}")
    return value


def get_engine():
    url = URL.create(
        drivername="postgresql+psycopg2",
        username=_required_env("DB_USER"),
        password=_required_env("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=_required_env("DB_NAME"),
    )
    return create_engine(url)


engine = get_engine()


def load_weather_data(table_name: str, df):
    df.to_sql(name=table_name, con=engine, if_exists="append", index=False)

    logging.info("OK: Dados carregados com sucesso\n")

    df_check = pd.read_sql(f"SELECT * FROM {table_name}", con=engine)
    logging.info(f"Total de registros na tabela: {len(df_check)}\n")
