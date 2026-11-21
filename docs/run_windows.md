# Windows запуск

Открой две CMD/PowerShell вкладки в папке проекта.

## Терминал 1 — backend
```bat
.venv\Scripts\activate
python -m uvicorn backend.main:app --reload
```

Открой http://127.0.0.1:8000/docs

## Терминал 2 — Streamlit
```bat
.venv\Scripts\activate
streamlit run app.py
```

## Проверка
- http://127.0.0.1:8000/ — API root
- http://127.0.0.1:8000/health — health check
- http://127.0.0.1:8000/docs — Swagger
- Streamlit URL, показанный в терминале

Если n8n не запущен, API будет работать, но запросы к Persona Builder, Interviewer и Expert выдадут сообщение о соединении.