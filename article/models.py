from django.db import models
from accounts.models import User
# Create your models here.
from django.conf import settings
from django_resized import ResizedImageField

subject_list = [
        ('일반','일반'),
        ('정보','정보'),
        ('사진','사진'),
        ('자랑','자랑'),
]


class Article(models.Model):

    title = models.CharField(max_length=80)
    content = models.TextField()
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank = False)
    updated_at = models.DateTimeField(auto_now=True, null=False, blank = False)
    subject = models.CharField(max_length=80, choices = subject_list)
    hits = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    
class Comment(models.Model):

    content = models.TextField()
    create_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE, related_name ="comments" )
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank = False)

    def __str__(self):
        return self.content
    
class PostImage(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE, related_name ="image")
    image = ResizedImageField(size = [1000,1000],upload_to="image", null=True, blank=True)
    image_original = models.ImageField(upload_to="image", null=True, blank=True)


class LikeArticle(models.Model):

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_name')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="article_like_user"
    )

class LikeComment(models.Model):

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_name')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comment_like_user"
    )

