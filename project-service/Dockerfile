FROM python:3.12-slim

WORKDIR /app

# تثبيت Poetry
RUN pip install --no-cache-dir poetry

# نسخ ملفات poetry أولاً (مهم للكاش)
COPY pyproject.toml poetry.lock ./

# تثبيت dependencies بدون إنشاء virtualenv
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# نسخ باقي الكود
COPY . .

# تشغيل الخدمة
CMD ["uvicorn", "app.api.api:app", "--host", "0.0.0.0", "--port", "8000"]
