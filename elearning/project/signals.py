from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=Assignment)
def TotalScore(sender,  created, instance, **kwargs):
    if created == False:
        try:
            accumulator =  Total.objects.get(user=instance.user)
            accumulator.total += instance.score
            accumulator.save()
        except:
            accumulator =  Total.objects.create(user=instance.user, total=instance.score)


