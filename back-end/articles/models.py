from datetime import datetime

import mongoengine

# from mongoengine import Document, fields
from django_mongoengine import Document, fields

from .validators import validate_image_extension


# File path for Images (relative to the media root)
# For future use
def article_image_upload_path(instance, filename):
    return f"Article/{instance.id}/image/{filename}"


# Create your models here.
class ScrapyItems(Document):
    url = fields.ListField(fields.URLField(unique=True), blank=False)
    title = fields.StringField(blank=False)
    content = fields.StringField(blank=False)
    tags = fields.ListField(fields.StringField(max_length=30, unique=True))
    published_date = fields.DateTimeField(blank=False)
    modified_date = fields.DateTimeField(blank=False)
    outlet = fields.StringField(blank=False, max_length=30)


class AiGeneratedArticle(Document):
    id = fields.ObjectIdField(primary_key=True)
    title = fields.StringField(blank=False, max_length=160)
    body = fields.StringField(blank=False)
    scraped_article = fields.ReferenceField(ScrapyItems, blank=False, reverse_delete_rule=mongoengine.NULLIFY)
    published_date = fields.DateTimeField(default=datetime.utcnow())
    tags = fields.ListField(fields.StringField(max_length=30, unique=True))
    reading_time = fields.IntField(default=0, min_value=0, blank=True)
    # For future use
    image_path = fields.StringField(blank=True, validation=validate_image_extension)

    def __str__(self):
        return f"{self.title}"


# class AiGeneratedArticleInfo(EmbeddedDocument):
#     article_id = fields.ReferenceField("AiGeneratedArticle", required=True, reverse_delete_rule=mongoengine.NULLIFY)
#     title = fields.StringField(required=True, max_length=160)
#     published_date = fields.DateTimeField(required=True)
#     tags = fields.ListField(fields.StringField(max_length=30, unique=True))
#     reading_time = fields.IntField(default=0, min_value=0)
#     # For future use
#     image_path = fields.StringField(validation=validate_image_extension)

#     def __str__(self):
#         return f"{self.title}"
