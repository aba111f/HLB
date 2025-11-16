from confluent_kafka import Consumer, KafkaException
import json
import django
import os
import logging
import sys
import asyncio

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_exchange.settings.settings')


django.setup()

from apps.users.models import User
from apps.books.models import Book
from apps.exchange_requests.models import ExchangeRequest

logger = logging.getLogger(__name__)

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'exchange_requests_group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(['exchange_requests', 'books'])

def run_consumer():
    try:
        print("Consumer is running and waiting for messages...")
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                logger.error(f"Kafka error: {msg.error()}")
                continue

            data = json.loads(msg.value().decode('utf-8'))
            topic = msg.topic()

            if topic == "exchange_requests":
                handle_exchange_request(data)
            elif topic == "books":
                handle_book(data)

            print(f"Received message: {msg.value()}",f"Message topic: {msg.topic()}")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

def handle_exchange_request(data):
    try:
        from_user = User.objects.get(email=data['from_email'])
        to_user = User.objects.get(email=data['to_email'])
        requested_book = Book.objects.get(id=data['requested_book_id'])
        offered_book = Book.objects.get(id=data.get('offered_book_id')) if data.get('offered_book_id') else None

        print("Creating ExchangeRequest in DB...")

        exchange_request = ExchangeRequest.objects.create(
            from_user=from_user,
            to_user=to_user,
            requested_book=requested_book,
            offered_book=offered_book,
            message=data.get('message', '')
        )
        logger.info(f"ExchangeRequest created in DB: {exchange_request.id}")
    except Exception as e:
        logger.error(f"Failed to create ExchangeRequest: {e}")

def handle_book(data):
    try:
        owner = User.objects.get(email=data['owner_email'])
        Book.objects.create(
            owner=owner,
            title=data['title'],
            author=data.get('author'),
            genre=data.get('genre'),
            condition=data.get('condition'),
            description=data.get('description'),
            availability=data.get('availability'),
            book_image=data.get('book_image')
        )
        logger.info(f"Book created in DB: {data['title']}")
    except Exception as e:
        logger.error(f"Failed to create Book: {e}")


if __name__ == "__main__":
    print("Starting consumer...") 

    try:
        asyncio.run(run_consumer())
    except KeyboardInterrupt:
        print("Consumer stopped manually.")