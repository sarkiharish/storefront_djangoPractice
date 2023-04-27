from django.dispatch import receiver
from core.signals import on_order_created

@receiver(on_order_created)
def on_order_created(sender, **kwargs):
    print(kwargs['order'])