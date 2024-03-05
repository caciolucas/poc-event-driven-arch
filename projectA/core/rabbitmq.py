import pika 
class RabbitMQPublisher:
    def __init__(self, host, port, username, password, queue_name):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.queue_name = queue_name

    def publish_message(self, message):
        connection = pika.BlockingConnection(
            pika.URLParameters(f'amqp://{self.username}:{self.password}@{self.host}:{self.port}/myvhost')
        )

        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)

        channel.basic_publish(exchange='',
                              routing_key=self.queue_name,
                              body=message)

        connection.close()
