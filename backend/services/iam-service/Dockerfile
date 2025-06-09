FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# تغییرات منابع apt برای جلوگیری از مشکلات شبکه
RUN echo "deb http://deb.debian.org/debian bookworm main" > /etc/apt/sources.list \
    && echo "deb http://deb.debian.org/debian bookworm-updates main" >> /etc/apt/sources.list \
    && echo "deb http://deb.debian.org/debian-security bookworm-security main" >> /etc/apt/sources.list \
    && apt-get update && apt-get install -y build-essential libpq-dev gcc && apt-get clean

# نصب پکیج‌ها از فایل requirements.txt
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# کپی سایر فایل‌ها به داخل Docker container
COPY . /app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
