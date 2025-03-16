"""
Модели для базы данных PostgreSQL
"""
from sqlmodel import SQLModel, Field, Column, ForeignKey, UniqueConstraint
from sqlalchemy import Integer, Numeric
from sqlalchemy.dialects.postgresql import JSONB
from pydantic import validator
from typing import Optional, List
from datetime import datetime, date


class UserSessions(SQLModel, table=True):
    """
    Модель для хранения данных о сессиях пользователей.
    """
    __tablename__ = "user_sessions"

    session_id: str = Field(primary_key=True)
    user_id: int
    start_time: datetime
    end_time: Optional[datetime]
    pages_visited: Optional[List[str]] = Field(sa_column=Column(JSONB))
    device: str
    actions: Optional[List[str]] = Field(sa_column=Column(JSONB))


class ProductPriceHistory(SQLModel, table=True):
    """
    Модель для хранения истории цен на продукты.
    """
    __tablename__ = "product_price_history"
    __table_args__ = (
        UniqueConstraint('product_id', 'date', name='unique_product_date'),
    )

    history_id: int | None = Field(
        None, sa_column=Column(Integer, primary_key=True, autoincrement=True, default=None),
    )
    product_id: int = Field(sa_column=Column(Integer, ForeignKey("product_current_price.product_id", ondelete="CASCADE")))
    price: float = Field(sa_column=Column(Numeric(10, 2)))
    currency: str = Field(max_length=10)
    date: date

    @validator('price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Цена должна быть положительной.")
        return value

class ProductCurrentPrice(SQLModel, table=True):
    """
    Модель для хранения текущей цены на продукты.
    """
    __tablename__ = "product_current_price"

    product_id: int = Field(primary_key=True)
    current_price: float = Field(sa_column=Column(Numeric(10, 2)))
    currency: str = Field(max_length=10)

    @validator('current_price')
    def validate_price(cls, value):
        if value < 0:
            raise ValueError("Цена должна быть положительной.")
        return value

class EventLogs(SQLModel, table=True):
    """
    Модель для хранения логов событий.
    """
    __tablename__ = "event_logs"

    event_id: str = Field(primary_key=True)
    timestamp: datetime
    event_type: str = Field(max_length=50)
    details: Optional[dict] = Field(sa_column=Column(JSONB))


class SupportTickets(SQLModel, table=True):
    """
    Модель для хранения данных о тикетах поддержки.
    """
    __tablename__ = "support_tickets"

    ticket_id: str = Field(primary_key=True)
    user_id: int
    status: str = Field(max_length=20)
    issue_type: str = Field(max_length=50)
    messages: Optional[dict] = Field(sa_column=Column(JSONB))
    created_at: datetime
    updated_at: datetime


class UserRecommendations(SQLModel, table=True):
    """
    Модель для хранения рекомендаций для пользователей.
    """
    __tablename__ = "user_recommendations"

    user_id: int = Field(primary_key=True)
    recommended_products: Optional[dict] = Field(sa_column=Column(JSONB))
    last_updated: datetime

class ModerationQueue(SQLModel, table=True):
    """
    Модель для хранения данных о модерации.
    """
    __tablename__ = "moderation_queue"

    review_id: str = Field(primary_key=True)
    user_id: int
    product_id: int = Field(sa_column=Column(Integer, ForeignKey("product_current_price.product_id", ondelete="CASCADE")))
    review_text: str
    rating: int
    moderation_status: str = Field(max_length=20)
    flags: Optional[dict] = Field(sa_column=Column(JSONB))
    submitted_at: datetime

    @validator('rating')
    def validate_rating(cls, value):
        if value < 1 or value > 5:
            raise ValueError("Рейтинг должен быть от 1 до 5.")
        return value


class SearchQueries(SQLModel, table=True):
    """
    Модель для хранения данных о поисковых запросах.
    """
    __tablename__ = "search_queries"

    query_id: str = Field(primary_key=True)
    user_id: int
    query_text: str
    timestamp: datetime
    filters: Optional[dict] = Field(sa_column=Column(JSONB))
    results_count: int
