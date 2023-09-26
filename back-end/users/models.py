from articles.models import AiGeneratedArticleInfo
from articles.validators import validate_image_extension
from cryptography import fernet
from djback.settings import PUBLIC_KEY
from mongoengine import Document, EmbeddedDocumentField, ValidationError, fields, signals


# File path for Images (relative to the media root)
def user_profile_picture_upload_path(instance, filename):
    return f"User/{instance.id}/profile_picture/{filename}"


# Create your models here.


class User(Document):
    id = fields.SequenceField(primary_key=True, unique=True)
    first_name = fields.StringField(required=True, max_length=20)
    last_name = fields.StringField(required=True, max_length=20)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True, min_length=8, max_length=20)
    avg_reading_time = fields.IntField(default=0, min_value=0)
    profile_picture = fields.ImageField(
        size=(None, 1024**2 * 1), validation=validate_image_extension, upload_to=user_profile_picture_upload_path
    )
    # We are using a hybrid approach to store the articles that the user has liked and disliked
    # Embedded documents contain the article info and the reference field contains the article id
    reading_list = fields.ListField(EmbeddedDocumentField(AiGeneratedArticleInfo), default=[])
    liked_articles = fields.ListField(EmbeddedDocumentField(AiGeneratedArticleInfo), default=[])
    disliked_articles = fields.ListField(EmbeddedDocumentField(AiGeneratedArticleInfo), default=[])

    # liked and disliked tags are stored separately for recommendation purposes
    liked_tags = fields.ListField(fields.StringField(max_length=30), default=[], unique=True)
    disliked_tags = fields.ListField(fields.StringField(max_length=30), default=[], unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        super.clean()

        # Addtional validations
        if self.profile_picture.width < 100 or self.profile_picture.height < 100:
            raise ValidationError("Image dimensions should be at least 100x100")

        # Ensure non-overlapping liked and disliked tags
        overlap = set(self.liked_tags) & set(self.disliked_tags)
        if overlap:
            raise ValidationError(f"Overlap found in liked and disliked tags: {overlap}")

        # Ensure non-overlapping liked and disliked tags
        overlap = set(self.liked_articles) & set(self.disliked_articles)
        if overlap:
            raise ValidationError(f"Overlap found in liked and disliked articles: {overlap}")

    # To ensure that the password is encrypted before saving (even if the user doesn't call the save method)
    def set_password(self, password):
        self.password = fernet.Fernet(PUBLIC_KEY).encrypt(password.encode())

    @classmethod
    def pre_delete(cls, sender, document, **kwargs):
        # Delete the profile picture when the user is deleted
        for field in document._fields.values():
            if isinstance(field, fields.ImageField):
                file = getattr(document, field.name)
                if file:
                    file.delete(save=False)

    def save(self, *args, **kwargs):
        self.clean()
        if self.id:
            existing = User.objects.get(id=self.id)
            # If the profile picture is being updated, then delete the old one
            if (existing is not None) and existing.profile_picture != self.profile_picture:
                existing.profile_picture.delete(save=False)
        # Encrypt password
        self.password = fernet.Fernet(PUBLIC_KEY).encrypt(self.password.encode())

        super().save(*args, **kwargs)


signals.pre_delete.connect(User.pre_delete, sender=User)  # Delete the profile picture when the user is deleted
