from django.forms import model_to_dict
import json

from core.rabbitmq import RabbitMQPublisher

#! Também poderia ficar salvo no signals.py
def retail_notify_post_save(sender, instance, created, **kwargs):
    publisher = RabbitMQPublisher('localhost', 5672, 'guest', 'guest', 'my_queue')

    action = 'save' 
    model = sender.__name__
    data = {
        'action': action,
        'app': sender._meta.app_label,
        'model': model,
        'data': model_to_dict(instance)
    }
    
    publisher.publish_message(json.dumps(data))