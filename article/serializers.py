from rest_framework import serializers
from .models import Article, Comment


class CommentSerializer(serializers.ModelSerializer):

    create_username = serializers.ReadOnlyField(source='create_user.username')

    class Meta:
        model = Comment
        fields=[
            'pk',
            'content',
            'create_username',
            'created_at',
            "article"
        ]

class ArticleInCommentSerializer(serializers.ModelSerializer):
    create_username = serializers.ReadOnlyField(source='create_user.username')

    class Meta:
        model = Comment
        fields = [
            'pk',
            'content',
            'create_username',
        ]

class ArticleSerializer(serializers.ModelSerializer):

    create_username = serializers.ReadOnlyField(source='create_user.username')
    comments = ArticleInCommentSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields=[
            "pk",
            'subject',
            'title',
            'content',
            'create_username',
            'created_at',
            "comments",
        ]

