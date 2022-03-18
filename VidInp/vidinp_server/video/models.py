from msilib import gen_uuid
from django.db import models
from .validators import file_size, process_file_size


class Video(models.Model):
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/%y", validators=[file_size])

    def __str__(self):
        return self.caption

class PVideoManager(models.Manager):
    def create_pro(self, id, caption, video):
        pro_vid = self.create(id=id, caption=caption, video=video)
        return pro_vid

class ProcessedVideo(models.Model):
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=100)
    video = models.FileField(
        upload_to="processed_video/%y", validators=[process_file_size]
    )

    objects = PVideoManager()


    def __str__(self):
        return self.caption
