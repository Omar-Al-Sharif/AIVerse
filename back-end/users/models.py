from articles.models import AiGeneratedArticleInfo
from mongoengine import Document, EmbeddedDocumentField, fields

# Create your models here.


class User(Document):
    id = fields.SequenceField(primary_key=True, unique=True)
    first_name = fields.StringField(required=True, max_length=20)
    last_name = fields.StringField(required=True, max_length=20)
    email = fields.EmailField(required=True, unique=True)
    password = fields.StringField(required=True, min_length=8, max_length=20)
    avg_reading_time = fields.IntField(default=0)
    image = fields.ImageField()
    # We are using a hybrid approach to store the articles that the user has liked and disliked
    # Embedded documents contain the article info and the reference field contains the article id
    reading_list = fields.ListField(EmbeddedDocumentField(AiGeneratedArticleInfo), default=[])
    liked_list = fields.ListField(EmbeddedDocumentField(AiGeneratedArticleInfo), default=[])
    disliked_articles = fields.ListField(EmbeddedDocumentField(AiGeneratedArticleInfo), default=[])
    liked_tags = fields.ListField(fields.StringField(max_length=30), default=[])
    disliked_tags = fields.ListField(fields.StringField(max_length=30), default=[])
