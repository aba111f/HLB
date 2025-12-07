from confluent_kafka import Producer
import json
import logging
import os

logger = logging.getLogger(__name__)

kafka_server = os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')

conf = {
    'bootstrap.servers': kafka_server
}

producer = Producer(conf)

def send_message(topic: str, message: dict):

    try:
        producer.produce(topic, json.dumps(message).encode('utf-8'))
        producer.flush()
        logger.info(f"Message sent to topic {topic}: {message}")
    except Exception as e:
        logger.error(f"Failed to send message to Kafka: {e}")
