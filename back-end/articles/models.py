import mongoengine
from mongoengine import Document, EmbeddedDocument, fields

# Create your models here.


class AiGeneratedArticle(Document):
    id = fields.SequenceField(primary_key=True, unique=True)
    title = fields.StringField(required=True, max_length=150)
    body = fields.StringField(required=True)
    original_article = fields.ReferenceField("Article", required=True, reverse_delete_rule=mongoengine.NULLIFY)
    published_date = fields.DateTimeField(required=True)
    tags = fields.ListField(fields.StringField(max_length=30))
    reading_time = fields.IntField(default=0)
    image_url = fields.ImageField()


class AiGeneratedArticleInfo(EmbeddedDocument):
    article_id = fields.ReferenceField("Article", required=True, reverse_delete_rule=mongoengine.CASCADE)
    title = fields.StringField(required=True, max_length=150)
    published_date = fields.DateTimeField(required=True)
    tags = fields.ListField(fields.StringField(max_length=30))
    reading_time = fields.IntField(default=0)
