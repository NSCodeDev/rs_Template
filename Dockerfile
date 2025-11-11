FROM python:3.13-slim

WORKDIR /app
# install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
# install dependencies
COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY . /app/

RUN chmod +x /app/entrypoint.sh

ENV PORT=8001
# expose the django port
EXPOSE 8001
# command to run django application
CMD ["./entrypoint.sh"]