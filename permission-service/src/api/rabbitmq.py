from faststream import FastStream
from faststream.rabbit import RabbitBroker, RabbitQueue
from src.settings import Settings, get_settings


settings: Settings = get_settings()
broker = RabbitBroker(url=str(settings.rabbitmq.dsn))
app = FastStream(broker)
request_queue = RabbitQueue("request", durable=True)
response_queue = RabbitQueue("response", durable=True)
