from django.db import models
from .validators import file_size, process_file_size


class Video(models.Model):
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=100)
    video = models.FileField(upload_to="video/%y", validators=[file_size])

    def __str__(self):
        return self.caption


class ProcessedVideo(models.Model):
    id = models.IntegerField(primary_key=True)
    caption = models.CharField(max_length=100)
    video = models.FileField(
        upload_to="processed_video/%y" 
    )

    def __str__(self):
        return self.caption
