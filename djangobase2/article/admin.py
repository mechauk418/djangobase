from django.contrib import admin
from .models import Article, Comment, PostImage, LikeArticle, LikeComment
# Register your models here.

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(PostImage)
admin.site.register(LikeComment)
admin.site.register(LikeArticle)