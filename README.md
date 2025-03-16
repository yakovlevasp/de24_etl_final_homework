# Проект по репликации данных из MongoDB в PostgreSQL

## Описание проекта
Данный проект предназначен для демонстрации ETL-процесса по репликации данных из базы данных MongoDB в PostgreSQL с использованием Apache Airflow. В рамках проекта выполняются следующие задачи:
- Генерация фейковых данных в MongoDB.
- Репликация данных из MongoDB в PostgreSQL.

## Используемые технологии
- **Apache Airflow** – для управления DAG-пайплайнами.
- **MongoDB** – в качестве исходной базы данных.
- **PostgreSQL** – в качестве целевой базы данных.
- **SQLModel** – для создания таблиц и валидации данных.

## Структура проекта
```
project_root/
│── dags/
│   ├── generate_dag.py  # DAG для генерации данных в MongoDB
│   ├── replicate_dag.py  # DAG для репликации данных в PostgreSQL
│── scripts/
│   ├── generate_mongodb_data.py  # Скрипт для генерации данных в MongoDB
│   ├── replicate_data.py  # Скрипт для репликации данных из MongoDB в PostgreSQL
|   ├── postgres_models.py  # Модели для базы данных PostgreSQL 
│── docker-compose.yml  # Контейнеризация проекта
│── requirements.txt  # Зависимости проекта
```

## Описание DAGs
### 1. mongodb_data_generator
DAG для генерации фейковых данных в MongoDB
Файл: `generate_dag.py`

- Создает фейковые данные для следующих коллекций:
    - UserSessions
    - EventLogs
    - SupportTickets
    - UserRecommendations
    - ModerationQueue
    - SearchQueries
    - ProductPriceHistory

**Запуск DAG:** происходит однократно (`@once`).

### 2. replicate_mongodb_to_postgres
DAG для репликации данных из MongoDB в PostgreSQL
Файл: `replicate_dag.py`

- Реплицирует данные из MongoDB в PostgreSQL для следующих таблиц:
    - UserSessions
    - EventLogs
    - SupportTickets
    - UserRecommendations
    - ModerationQueue
    - SearchQueries
    - ProductPriceHistory
    - ProductCurrentPrice

**Запуск DAG:** выполняется ежедневно (`@daily`).

## Установка и запуск проекта
### 1. Запуск через Docker Compose
```sh
docker-compose up -d
```

### 2. Доступ к веб-интерфейсу Airflow
Перейдите в браузере по адресу:
```
http://localhost:8080
```

### 3. Запуск DAGs
В веб-интерфейсе Airflow активируйте и запустите DAG `mongodb_data_generator`, затем DAG `replicate_mongodb_to_postgres`.
