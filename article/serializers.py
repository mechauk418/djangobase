from rest_framework import serializers
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields=[
            'subject',
            'title',
            'content',
            'create_user',
            'created_at',
        ]

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields=[
            'content',
            'create_user',
            'created_at',
        ]