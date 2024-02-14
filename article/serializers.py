from rest_framework import serializers
from .models import Article, Comment, PostImage


class CommentSerializer(serializers.ModelSerializer):

    create_username = serializers.ReadOnlyField(source='create_user.username')
    # article = serializers.ReadOnlyField(source='article.pk')

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


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = [
            'image',
            'image_original'
        ]

class ArticleSerializer(serializers.ModelSerializer):

    create_username = serializers.ReadOnlyField(source='create_user.username')
    comments = ArticleInCommentSerializer(many=True, read_only=True)
    images = serializers.SerializerMethodField()

    def get_images(self,obj):
        image = obj.image.all()
        return PostImageSerializer(instance=image, many=True, context = self.context).data

    class Meta:
        model = Article
        fields=[
            "pk",
            'subject',
            'title',
            'content',
            'create_username',
            "hits",
            'created_at',
            "comments",
            "images"
        ]

    def create(self, validated_data):
        instance = Article.objects.create(**validated_data)
        image_set = self.context['request'].FIELS
        for image_data in image_set.getlist('image'):
            ext = str(image_data).split('.')[-1]
            ext = ext.lower()
            if ext in ['jpg', 'jpeg','png',]:
                PostImage.objects.create(article=instance, image=image_data, image_original=image_data)
            elif ext in ['gif','webp']:
                PostImage.objects.create(article=instance, image_original=image_data)
        return instance
