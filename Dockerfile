FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    fonts-liberation libnss3 libatk-bridge2.0-0 libgtk-3-0 \
    libxss1 libasound2 libxshmfence1 libgbm1 libxrandr2 \
    libatk1.0-0 libcups2 libdrm2 libxcomposite1 libxdamage1 \
    libpango-1.0-0 libpangocairo-1.0-0

# Add PostgreSQL 16 repo and install client 16 (use bookworm-pgdg, not bullseye-pgdg)
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    echo "deb http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    apt-get update && \
    apt-get install -y postgresql-client-16 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

RUN playwright install --with-deps

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "-m", "scheduler.scheduler"]
