from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Purchase, Course, User

@receiver(m2m_changed, sender=User.courses.through)
def create_purchase(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == "post_add" and not reverse:
        user = instance
        for pk in pk_set:
            course = Course.objects.get(pk=pk)
            Purchase.objects.create(student=user, course=course)
