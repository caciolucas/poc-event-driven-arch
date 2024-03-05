import pika
import json
from django.apps import apps

PROJECT_APPS_MAPPER = {
    "core": {
        "Product": ("core", "Product"),
        "Store": ("core", "Store")
    }
}

class RabbitMQConsumer:
    def __init__(self, amqp_url, queue_name):
        self.amqp_url = amqp_url
        self.queue_name = queue_name
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(
            parameters=pika.URLParameters(self.amqp_url)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
    
    def _get_model(self, _app, _model):
        app, model = PROJECT_APPS_MAPPER[_app][_model]
        return apps.get_model(app, model)
    
    def _parse_message(self, body, method):
        try:
            message = json.loads(body)
        except json.JSONDecodeError:
            print(f"Invalid message: {body}")
            self.channel.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            return
        return message
        
    def _parse_message_payload(self, message):
        try:
            action = message['action']
            app = message['app']
            model = message['model']
            data = message['data']
        except KeyError:
            print(f"Invalid message: {message}")
            return
        
        return (action, app, model, data)
    
    def _clean_data(self, Model, data):
        cleaned_data = {}
        for key in data.keys():
            if Model._meta.get_field(key).get_internal_type() == "ForeignKey":
                cleaned_data[key + '_id'] = data[key]
            else:
                cleaned_data[key] = data[key]
        return cleaned_data

    def _save_model(self, Model, data):
        cleaned_data = self._clean_data(Model, data)
        return  Model.objects.update_or_create(
            id=data['id'],
            defaults=cleaned_data
        )
    
    def callback(self, ch, method, properties, body):
        message = self._parse_message(body, method)
        
        if not message:
            return
        
        action, app, model, data = self._parse_message_payload(message)

        Model = self._get_model(app, model)

        try:
            if action == 'save':
                print(f"== Performing save action on {model} with data: {data}")
                obj, created = self._save_model(Model, data)
                
                print(f"Object {'created' if created else 'updated'}: {obj}")
            else:
                print(f"== Invalid action: {action}")

        except Exception as e:
            print(f"Error: {e}")
            ch.basic_reject(delivery_tag=method.delivery_tag, requeue=False)
            return

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        try:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
            print("== Consumer started")
            self.channel.start_consuming()
        except KeyboardInterrupt:
            print("== Consumer ended")
            
rabbitMQ_consumer = RabbitMQConsumer('amqp://guest:guest@localhost:5672/myvhost', 'my_queue')
rabbitMQ_consumer.connect()
rabbitMQ_consumer.start_consuming()
