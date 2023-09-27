from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from .models import AiGeneratedArticle, ScrapyItems
from .serializers import AiGeneratedArticleSerializer, ScrapedArticleSerializer

# Create your views here.


# What shall we do here?
# Create a view for Creating an AI generated article
class AiGeneratedArticleViewSet(viewsets.ModelViewSet):
    serializer_class = AiGeneratedArticleSerializer
    queryset = AiGeneratedArticle.objects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        tags = request.query_params.get("tags")
        page = request.query_params.get("page")
        items_per_page = request.query_params.get("items")

        # Filtering by tags
        if tags:
            tags = tags.split(",")
            self.queryset = queryset(tags__in=tags)

        # Pagination
        if page and items_per_page:
            queryset = queryset.fields(slice_comment=[(int(page) - 1) * int(items_per_page), int(items_per_page)])

        serializer = AiGeneratedArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=200)


class ScrapedArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ScrapedArticleSerializer
    queryset = ScrapyItems.objects

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        tags = request.query_params.get("tags")

        # Filtering by tags
        if tags:
            tags = tags.split(",")
            self.queryset = queryset(tags__in=tags)

        serializer = ScrapedArticleSerializer(queryset, many=True)
        return Response(serializer.data, status=200)
