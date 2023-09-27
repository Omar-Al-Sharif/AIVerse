from rest_framework_mongoengine import serializers

from .models import AiGeneratedArticle, ScrapyItems


class AiGeneratedArticleSerializer(serializers.DocumentSerializer):
    class Meta:
        model = AiGeneratedArticle
        exclude = ["published_date"]


class ScrapedArticleSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ScrapyItems
        fields = "__all__"
