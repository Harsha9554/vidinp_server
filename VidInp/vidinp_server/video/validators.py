from django.core.exceptions import ValidationError


def file_size(value):
    file_size = value.size
    if file_size > 419430400:
        raise ValidationError("maximum size is 50MB")


def process_file_size(value):
    file_size = value.size
    if file_size == 0:
        raise ValidationError("it's empty video")
