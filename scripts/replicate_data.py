"""
Репликация данных из MongoDB в PostgreSQL
"""
import logging

import pandas as pd
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from pymongo import MongoClient

import postgres_models

BATCH_SIZE = 2000

def replicate_table(table_name: str):
    """
    Реплицирует данные из указанной коллекции MongoDB в PostgreSQL
    """
    client = MongoClient('mongodb')
    db = client['analytics_db']
    collection = db[table_name]

    postgres_model = getattr(postgres_models, table_name)
    engine = create_engine('postgresql+psycopg2://app:app@postgres-app:5432/products')
    session_builder = sessionmaker(bind=engine)

    postgres_model.__table__.create(engine, checkfirst=True)

    with session_builder() as session:
        session.query(postgres_model).delete()
        session.commit()

    skip = 0
    while True:
        cursor = collection.find({}).skip(skip).limit(BATCH_SIZE)
        batch = list(cursor)
        if not batch:
            break

        df = pd.DataFrame(batch)
        if df.empty:
            break

        with session_builder() as session:
            validate_rows = []
            for _, row in df.iterrows():
                try:
                    validate_rows.append(
                        postgres_model.validate(row.to_dict()).dict()
                    )
                except ValidationError as e:
                    logging.warning(f"Пропущена запись: {row}. Ошибка: {e}")

            if validate_rows:
                stmt = insert(postgres_model).values(validate_rows).on_conflict_do_nothing()
                session.execute(stmt)
                session.commit()

        skip += BATCH_SIZE

def replicate_product_price_history():
    """
    Реплицирует данные из коллекции ProductPriceHistory в PostgreSQL
    """
    client = MongoClient('mongodb')
    db = client['analytics_db']
    collection = db.ProductPriceHistory

    engine = create_engine('postgresql+psycopg2://app:app@postgres-app:5432/products')
    session_builder = sessionmaker(bind=engine)

    postgres_models.ProductCurrentPrice.__table__.create(engine, checkfirst=True)
    postgres_models.ProductPriceHistory.__table__.create(engine, checkfirst=True)

    with session_builder() as session:
        session.query(postgres_models.ProductCurrentPrice).delete()
        session.query(postgres_models.ProductPriceHistory).delete()
        session.commit()

    skip = 0
    while True:
        cursor = collection.find({}).skip(skip).limit(BATCH_SIZE)
        batch = list(cursor)
        if not batch:
            break

        df = pd.DataFrame(batch)
        if df.empty:
            break

        with session_builder() as session:
            price_history_data = []
            current_price_data = []

            for _, row in df.iterrows():
                price_history_dates = set()
                for price_change in row['price_changes']:
                    price_change['date'] = price_change['date'].date()
                    if price_change['date'] in price_history_dates:
                        logging.warning(f"Дублирующаяся запись в ProductPriceHistory: {price_change}, product_id: {row['product_id']}.")
                        continue
                    price_history_dates.add(price_change['date'])

                    try:
                        price_history = postgres_models.ProductPriceHistory.validate(
                            {"product_id": row['product_id'], **price_change}
                        ).dict()
                    except ValidationError as e:
                        logging.warning(f"Пропущена запись в ProductPriceHistory: {price_change}. Ошибка: {e}")

                    del price_history['history_id']
                    price_history_data.append(price_history)

                try:
                    current_price_data.append(
                        postgres_models.ProductCurrentPrice.validate(row.to_dict()).dict()
                    )
                except ValidationError as e:
                    logging.warning(f"Пропущена запись: {row}. Ошибка: {e}")

            if current_price_data:
                stmt = insert(postgres_models.ProductCurrentPrice).values(current_price_data).on_conflict_do_nothing()
                session.execute(stmt)
            if price_history_data:
                stmt = insert(postgres_models.ProductPriceHistory).values(price_history_data).on_conflict_do_nothing()
                session.execute(stmt)
            session.commit()

        skip += BATCH_SIZE
