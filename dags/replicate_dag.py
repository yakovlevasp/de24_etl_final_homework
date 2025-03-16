"""
DAG для репликации данных из MongoDB в PostgreSQL
"""
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models.baseoperator import chain
from pydantic.class_validators import partial

from scripts.replicate_data import replicate_table, replicate_product_price_history

with DAG(
        'replicate_mongodb_to_postgres',
        description='Репликация данных из MongoDB в PostgreSQL',
        schedule_interval='@daily',
        start_date=datetime(2025, 1, 1),
        catchup=False
) as dag:
    tasks = [
        PythonOperator(
            task_id=f'replicate_{name}',
            python_callable=func
        )
        for name, func in (
            ('user_sessions', partial(replicate_table, table_name='UserSessions')),
            ('product_price_history', replicate_product_price_history),
            ('event_logs', partial(replicate_table, table_name='EventLogs')),
            ('support_tickets', partial(replicate_table, table_name='SupportTickets')),
            ('user_recommendations', partial(replicate_table, table_name='UserRecommendations')),
            ('moderation_queue', partial(replicate_table, table_name='ModerationQueue')),
            ('search_queries', partial(replicate_table, table_name='SearchQueries'))
        )
    ]
    chain(*tasks)
