from content.tasks import convert_360p, convert_480p, convert_720p, convert_1080p
from .models import Video
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video is saved')
    if created:
        print('new Video is created')
        convert_360p.delay(instance.video_file.path)
        convert_480p.delay(instance.video_file.path)
        convert_720p.delay(instance.video_file.path)
        convert_1080p.delay(instance.video_file.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('Video is deleted')
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)