# ModeusAristo

Проект для исследования профессиональной деятельности: источники → факты → синтетическая персона → интервью AI Interviewer/AI Expert.

## Структура
- `app.py` — Streamlit UI
- `backend/main.py` — FastAPI API
- `backend/n8n_client.py` — клиент n8n webhooks
- `backend/services/facts_builder.py` — сбор фактов из SQLite
- `database/db_manager.py` — SQLite storage
- `n8n/` — экспорт workflow

## Запуск
1. Создать окружение: `python -m venv .venv`
2. Активировать: Windows `.venv\\Scripts\\activate`
3. Установить: `pip install -r requirements.txt`
4. Запустить API: `python -m uvicorn backend.main:app --reload`
5. В отдельном терминале: `streamlit run app.py`

API docs: http://127.0.0.1:8000/docs

## n8n
Ожидаются webhooks:
- `POST /webhook/persona`
- `POST /webhook/<interviewer-workflow-id>`
- `POST /webhook/persona/respond`

Для тестовых URL измените адреса в `backend/n8n_client.py`. В n8n Webhook nodes используйте Respond = Using Respond to Webhook Node, а Respond to Webhook должен возвращать JSON-объект, не JSON-строку.

## Примечание
В репозитории не хранятся credentials, локальные базы данных или `.env`.