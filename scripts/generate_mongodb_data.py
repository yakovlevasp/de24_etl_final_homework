"""
Генерация данных для MongoDB
"""
import random

from faker import Faker
from pymongo import MongoClient


DB_NAME = "analytics_db"


def clean_database() -> None:
    """
    Очистка данных в БД
    """
    client = MongoClient('mongodb')
    client.drop_database(DB_NAME)


def generate_user_sessions() -> None:
    """
    Генерация данных для коллекции UserSessions
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    collection = db.UserSessions
    fake = Faker()
    data = [{
        "session_id": fake.uuid4(),
        "user_id": random.randint(1, 100),
        "start_time": fake.date_time_this_year(),
        "end_time": fake.date_time_this_year(),
        "pages_visited": [fake.uri() for _ in range(random.randint(1, 10))],
        "device": fake.user_agent(),
        "actions": [fake.word() for _ in range(random.randint(1, 5))]
    } for _ in range(5000)]
    collection.insert_many(data)


def generate_product_price_history() -> None:
    """
    Генерация данных для коллекции ProductPriceHistory
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    fake = Faker()
    collection = db.ProductPriceHistory
    data = [{
        "product_id": product_id,
        "price_changes": [
            {
                "date": fake.date_time_this_year(),
                "price": round(random.uniform(10, 500), 2),
                "currency": "USD"
            } for _ in range(5)
        ],
        "current_price": round(random.uniform(10, 500), 2),
        "currency": "USD"
    } for product_id in range(5000)]
    collection.insert_many(data)


def generate_event_logs() -> None:
    """
    Генерация данных для коллекции EventLogs
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    fake = Faker()
    collection = db.EventLogs
    data = [{
        "event_id": fake.uuid4(),
        "timestamp": fake.date_time_this_year(),
        "event_type": fake.word(),
        "details": fake.sentence()
    } for _ in range(5000)]
    collection.insert_many(data)


def generate_support_tickets() -> None:
    """
    Генерация данных для коллекции SupportTickets
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    fake = Faker()
    collection = db.SupportTickets
    data = [{
        "ticket_id": fake.uuid4(),
        "user_id": random.randint(1, 100),
        "status": random.choice(["open", "closed", "pending"]),
        "issue_type": fake.word(),
        "messages": [fake.sentence() for _ in range(random.randint(1, 5))],
        "created_at": fake.date_time_this_year(),
        "updated_at": fake.date_time_this_year()
    } for _ in range(5000)]
    collection.insert_many(data)


def generate_user_recommendations() -> None:
    """
    Генерация данных для коллекции UserRecommendations
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    fake = Faker()
    collection = db.UserRecommendations
    data = [{
        "user_id": fake.uuid4(),
        "recommended_products": [random.randint(1, 4999) for _ in range(random.randint(1, 5))],
        "last_updated": fake.date_time_this_year()
    } for _ in range(5000)]
    collection.insert_many(data)


def generate_moderation_queue() -> None:
    """
    Генерация данных для коллекции ModerationQueue
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    fake = Faker()
    collection = db.ModerationQueue
    data = [{
        "review_id": fake.uuid4(),
        "user_id": random.randint(1, 100),
        "product_id": random.randint(1, 4999),
        "review_text": fake.text(),
        "rating": random.randint(1, 5),
        "moderation_status": random.choice(["pending", "approved", "rejected"]),
        "flags": [fake.word() for _ in range(random.randint(0, 3))],
        "submitted_at": fake.date_time_this_year()
    } for _ in range(5000)]
    collection.insert_many(data)


def generate_search_queries() -> None:
    """
    Генерация данных для коллекции SearchQueries
    """
    client = MongoClient('mongodb')
    db = client[DB_NAME]
    fake = Faker()
    collection = db.SearchQueries
    data = [{
        "query_id": fake.uuid4(),
        "user_id": random.randint(1, 100),
        "query_text": fake.word(),
        "timestamp": fake.date_time_this_year(),
        "filters": {fake.word(): fake.word() for _ in range(random.randint(1, 3))},
        "results_count": random.randint(0, 100)
    } for _ in range(5000)]
    collection.insert_many(data)
