from django.contrib import admin
from .models import ProcessedVideo, Video

# Register your models here.
admin.site.register(Video)
admin.site.register(ProcessedVideo)
