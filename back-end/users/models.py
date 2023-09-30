import os

import mongoengine
from articles.models import AiGeneratedArticle
from articles.validators import validate_image_extension

# from cryptography import fernet
from django.conf import settings
from django_mongoengine import Document, fields
from django_mongoengine.mongo_auth.models import AbstractUser, MongoUser
from dotenv import load_dotenv
from mongoengine import ValidationError, signals

load_dotenv()
PUBLIC_KEY = bytes(os.getenv("PUBLIC_KEY"), "utf-8")


# File path for Images (relative to the media root)
def user_profile_picture_upload_path(instance, filename):
    return f"User/{instance.id}/profile_picture/{filename}"


# Create your models here.


class User(MongoUser):
    # id = fields.ObjectIdField(primary_key=True)
    username = fields.StringField(blank=True, max_length=30, unique=True)
    full_name = fields.StringField(blank=False, max_length=50)
    email = fields.EmailField(blank=False, unique=True)
    password = fields.StringField(blank=False)
    avg_reading_time = fields.IntField(default=0, min_value=0, blank=True)
    profile_picture = fields.StringField(validation=validate_image_extension, blank=True)

    # Note when joining these lists with AiGeneratedArticle, project the content field to None if it wasn't needed
    reading_list = fields.ListField(fields.ReferenceField(AiGeneratedArticle), default=[], blank=True)
    liked_articles = fields.ListField(fields.ReferenceField(AiGeneratedArticle), default=[], blank=True)
    disliked_articles = fields.ListField(fields.ReferenceField(AiGeneratedArticle), default=[], blank=True)
    current_feed = fields.ListField(fields.ReferenceField(AiGeneratedArticle), default=[], blank=True)
    # liked and disliked tags are stored separately for recommendation purposes
    liked_tags = fields.ListField(fields.StringField(max_length=30), default=[], blank=True)
    disliked_tags = fields.ListField(fields.StringField(max_length=30), default=[], blank=True)

    is_active = fields.BooleanField(default=True, blank=True)
    is_staff = fields.BooleanField(default=False, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "password"]

    def __str__(self):
        return f"{self.full_name}"

    def clean(self):
        # Ensure non-overlapping liked and disliked tags
        overlap = set(self.liked_tags) & set(self.disliked_tags)
        if overlap:
            raise ValidationError(f"Overlap found in liked and disliked tags: {overlap}")

        # Ensure non-overlapping liked and disliked tags
        overlap = set(self.liked_articles) & set(self.disliked_articles)
        if overlap:
            raise ValidationError(f"Overlap found in liked and disliked articles: {overlap}")

    # To ensure that the password is encrypted before saving (even if the user doesn't call the save method)
    # def set_password(self, password):
    #     self.password = fernet.Fernet(settings.PUBLIC_KEY).encrypt(self.password.encode())

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        # Delete the profile picture when the user is deleted
        os.remove(os.path.join(settings.MEDIA_ROOT, document.profile_picture))

    def save(self, *args, **kwargs):
        self.clean()
        if self.id:
            existing = User.objects(id=self.id)
            # If the profile picture is being updated, then delete the old one
            if (existing.first() is not None) and existing.first().profile_picture != self.profile_picture:
                existing.profile_picture.delete(save=False)
        # Encrypt password
        # self.password = str(fernet.Fernet(PUBLIC_KEY).encrypt(self.password.encode("utf-8")))
        return super().save(*args, **kwargs)
        # super().save(*args, **kwargs)

    # check the password
    # def check_password(self, password):
    #     return fernet.Fernet(PUBLIC_KEY).decrypt(self.password.encode("utf-8")).decode("utf-8") == password


class Playlist(Document):
    # id = fields.SequenceField(primary_key=True, unique=True)
    name = fields.StringField(blank=False, max_length=30)
    user = fields.ReferenceField(User, blank=False, reverse_delete_rule=mongoengine.CASCADE)
    articles = fields.ListField(fields.ReferenceField(AiGeneratedArticle, blank=False), default=[])

    def __str__(self):
        return f"{self.name}"


signals.pre_delete.connect(User.pre_delete, sender=User)  # Delete the profile picture when the user is deleted
