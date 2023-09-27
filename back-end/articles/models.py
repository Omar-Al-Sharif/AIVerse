from datetime import datetime

import mongoengine
from mongoengine import Document, fields

from .validators import validate_image_extension


# File path for Images (relative to the media root)
# For future use
def article_image_upload_path(instance, filename):
    return f"Article/{instance.id}/image/{filename}"


# Create your models here.
class ScrapyItems(Document):
    url = fields.ListField(fields.URLField(unique=True), required=True)
    title = fields.StringField(required=True)
    content = fields.StringField(required=True)
    tags = fields.ListField(fields.StringField(max_length=30, unique=True))
    published_date = fields.DateTimeField(required=True)
    modified_date = fields.DateTimeField(required=True)
    outlet = fields.StringField(required=True, max_length=30)


class AiGeneratedArticle(Document):
    title = fields.StringField(required=True, max_length=160)
    body = fields.StringField(required=True)
    scraped_article = fields.ReferenceField(ScrapyItems, required=True, reverse_delete_rule=mongoengine.NULLIFY)
    published_date = fields.DateTimeField(default=datetime.utcnow())
    tags = fields.ListField(fields.StringField(max_length=30, unique=True))
    reading_time = fields.IntField(default=0, min_value=0, required=False)
    # For future use
    image_path = fields.StringField(required=False, validation=validate_image_extension)

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
