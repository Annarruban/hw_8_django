from django.db.models.signals import pre_save
from django.dispatch import receiver

from app.models import Task
from app.utils import send_email


@receiver(pre_save, sender=Task)
def notify_owner_on_new_task(sender, instance, **kwargs):
    old_instance = sender.objects.filter(pk=instance.pk).first()
    if old_instance and old_instance.status != instance.status:
        send_email(
            'Status {instance.title} Changed',
            f'Status of task {instance.title} has changed: from {old_instance.status} to {instance.status}',
            instance.owner.email
        )