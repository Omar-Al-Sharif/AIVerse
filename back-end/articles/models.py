import mongoengine
from mongoengine import Document, EmbeddedDocument, fields
from validators import validate_image_extension

# Create your models here.


class AiGeneratedArticle(Document):
    id = fields.SequenceField(primary_key=True, unique=True)
    title = fields.StringField(required=True, max_length=160)
    body = fields.StringField(required=True)
    original_article = fields.ReferenceField("Article", required=True, reverse_delete_rule=mongoengine.NULLIFY)
    published_date = fields.DateTimeField(required=True)
    tags = fields.ListField(fields.StringField(max_length=30, unique=True))
    reading_time = fields.IntField(default=0, min_value=0)
    image_url = fields.ImageField(size=(None, 1024**2 * 2), validation=validate_image_extension)

    def __str__(self):
        return f"{self.title}"


class AiGeneratedArticleInfo(EmbeddedDocument):
    article_id = fields.ReferenceField("Article", required=True, reverse_delete_rule=mongoengine.CASCADE)
    title = fields.StringField(required=True, max_length=160)
    published_date = fields.DateTimeField(required=True)
    tags = fields.ListField(fields.StringField(max_length=30, unique=True))
    reading_time = fields.IntField(default=0, min_value=0)
    image_url = fields.ImageField(size=(None, 1024**2 * 2), validation=validate_image_extension)  # Max size 2MB

    def __str__(self):
        return f"{self.title}"
