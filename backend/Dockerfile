FROM python:3.11-slim

RUN apt-get update && apt-get install -y \ 
    netcat-openbsd gcc libpq-dev curl && \
    apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./book_exchange /app/

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]