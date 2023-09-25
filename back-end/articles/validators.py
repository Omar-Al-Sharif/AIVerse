import os

from mongoengine import ValidationError


def validate_image_extension(image):
    extension = os.path.splitext(image.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg", ".svg"]
    if extension.lower() not in valid_extensions:
        raise ValidationError(
            f"Image extension must be one of the following: {valid_extensions} But you uploaded {extension}"
        )
