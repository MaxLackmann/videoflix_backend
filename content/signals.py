from content.tasks import convert_480p, convert_720p, convert_1080p
from .models import Video
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import os

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):
    print('Video is saved')
    if created:
        print('new Video is created')
        convert_480p.delay(instance.video_file.path)
        convert_720p.delay(instance.video_file.path)
        convert_1080p.delay(instance.video_file.path)

@receiver(post_delete, sender=Video)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    print('Video is deleted')
    base_path = instance.video_file.path

    variants = [
        base_path,
        base_path.replace(".mp4", "_480p.mp4"),
        base_path.replace(".mp4", "_720p.mp4"),
        base_path.replace(".mp4", "_1080p.mp4"),
    ]

    for file_path in variants:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Gelöscht: {file_path}")
        else:
            print(f"Nicht gefunden: {file_path}")