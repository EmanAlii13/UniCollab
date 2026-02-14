# =========================
# Dockerfile للـ CLI
# =========================
FROM python:3.12-slim

# =========================
# منع python من كتابة pyc ونسخ الملفات
# =========================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# =========================
# نسخ متطلبات الـ CLI وتثبيتها
# =========================
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# =========================
# نسخ ملفات الـ CLI
# =========================
COPY . .

# =========================
# تشغيل الـ CLI
# =========================
CMD ["python", "main.py"]
