"""
DAG для генерации фейковых данных в MongoDB
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain

from scripts.generate_mongodb_data import (
    clean_database,
    generate_user_sessions,
    generate_event_logs,
    generate_support_tickets,
    generate_user_recommendations,
    generate_moderation_queue,
    generate_search_queries,
    generate_product_price_history
)


with DAG(
        'mongodb_data_generator',
        description='Генерация фейковых данных в MongoDB',
        schedule_interval='@once',
        start_date=datetime(2025, 1, 1),
        catchup=False
) as dag:
    tasks = [
        PythonOperator(
            task_id=func.__name__,
            python_callable=func
        )
        for func in (
            clean_database,
            generate_user_sessions,
            generate_event_logs,
            generate_support_tickets,
            generate_user_recommendations,
            generate_moderation_queue,
            generate_search_queries,
            generate_product_price_history
        )
    ]
    chain(*tasks)
