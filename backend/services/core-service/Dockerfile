FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN rm -rf /etc/apt/sources.list.d/* \
    && echo "deb http://mirror.arvancloud.ir/debian/ bookworm main contrib non-free" > /etc/apt/sources.list \
    && echo "deb http://mirror.arvancloud.ir/debian-security bookworm-security main contrib non-free" >> /etc/apt/sources.list \
    && echo "deb http://mirror.arvancloud.ir/debian/ bookworm-updates main contrib non-free" >> /etc/apt/sources.list \
    && apt-get update --allow-releaseinfo-change \
    && apt-get install -y libpq-dev gcc \
    && apt-get install -y build-essential || apt-get install -f -y \
    && apt-get clean

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8010

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8010", "--reload"]
