from .models import ProcessedVideo, Video
from django import forms


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ("id", "caption", "video")


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ("id",)
