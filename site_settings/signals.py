from django.db.models.signals import post_delete
from django.dispatch import receiver

from site_settings.models import CarouselImage


@receiver(post_delete, sender=CarouselImage)
def post_delete_image(sender, instance, *args, **kwargs):
    instance.image.delete(save=False)
