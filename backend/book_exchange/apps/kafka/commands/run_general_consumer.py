from django.core.management.base import BaseCommand
from Book_Exchange.backend.book_exchange.apps.kafka.consumers.consumer_general import start_consumer

class Command(BaseCommand):
    help = "Run Kafka consumer for exchange_requests"

    def handle(self, *args, **kwargs):
        start_consumer()
