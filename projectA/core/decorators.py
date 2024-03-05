from django.db.models.signals import post_save
from core.functions import retail_notify_post_save

def retail_notify_changes(model_cls):
    post_save.connect(retail_notify_post_save, sender=model_cls)
    return model_cls
